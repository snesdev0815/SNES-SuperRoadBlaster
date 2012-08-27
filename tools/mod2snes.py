#!/usr/bin/env python

import os
import sys
import math
import logging

BRR_BLOCK_SAMPLES = 16
BRR_BLOCK_LENGTH = 9

BRR_ONE_SHOT_EXTEND = 25	#someone said non-looping samples are cut out 25 samples before their actual end. Adding these doesn't hurt, I guess...
BRR_MAX_RANGE_SHIFT	= 13
BRR_FILTERS = 4
SAMPLE_CUT_THRESHOLD = 256	#cut looping samples above this size instead of multipliying their size to make them divisible by 16

MOD_CHANNELS = 4
MOD_BYTES_PER_CHANNEL = 4
MOD_ROWS_PER_PATTERN = 64
MOD_PERIODS_PER_OCTAVE = 12
MOD_INSTRUMENT_DATA = 20
MOD_INSTRUMENT_DATA_LENGTH = 30
MOD_INSTRUMENT_COUNT = 31

#file offsets, converted modfile
SPCMOD_INSTRUMENT_DATA	= 0
SPCMOD_SONG_LENGTH		= 248
SPCMOD_PATTERN_COUNT	= 249
SPCMOD_SEQUENCE			= 250
SPCMOD_PATTERN_POINTER	= 378
SPCMOD_PATTERN_DATA		= 508

SPCMOD_EMPTY_CHANNEL	= 0xff
SPCMOD_INVALID_PERIOD	= 0xff

INSTR_RES_MULTI = 1

globalSampleBuffer = {
  'last'		: 0,
  'beforeLast'	: 0
}

statistics = {
  'samples'	: 0,
  'filter'	: { 0:0,1:0,2:0,3:0 },
  'range'	: { 0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0 },
  'maxError': 0,
  'minError': BRR_BLOCK_SAMPLES * 0xffff
}

#debugfile = open('debug.log', 'wb')
#debugfile.close()
logging.basicConfig( #filename='debug.log',
                    level=logging.INFO,
                    format='%(message)s')


def main():
    if len( sys.argv ) != 3:
      logging.info( 'Pro tracker MOD to SNES format converter' )
      logging.info( '2011-01-02 d4s matt@dforce3000.de' )
      logging.info( 'Usage:' )
      logging.info( '%s infile outfilebase' % sys.argv[0] )
      sys.exit(1)
      

    inFileName = sys.argv[1]
    outFileName = ( '%s.spcmod' % sys.argv[2] )

    try:
      inFile = open( inFileName, 'rb' )
    except IOError:
      logging.error( 'unable to access input file %s' % inFileName )
      sys.exit(1)

    try:
      outFile = open( outFileName, 'wb' )
    except IOError:
      logging.error( 'unable to access output file %s' % outFileName )
      sys.exit(1)

    inFileData = inFile.read()

    logging.debug( 'module files accessed successfully' )
    
    if not isValidModule( inFileData ):
      logging.error( '%s is not a valid MOD file.' % inFileName )
      sys.exit(1)
    
    moduleData = {}
    moduleData['name']				= getModuleName( inFileData )
    moduleData['length']			= getModuleLength( inFileData )
    moduleData['sequence']			= getModulePlaySequence( inFileData )
    moduleData['patternCount']		= getModulePatternCount( moduleData['sequence'] )
    moduleData['sampleBufferPos']	= getModuleSampleBufferPosition( moduleData['patternCount'] )
    moduleData['instruments']		= getModuleInstruments( inFileData, moduleData['sampleBufferPos'] )
    moduleData['patterns']			= getModulePatterns( inFileData, moduleData['patternCount'] )
    
    #debugLog( moduleData['instruments'] )
    convertedModule = {
      'length'			: moduleData['length'],
      'patternCount'	: moduleData['patternCount'],
      'sequence'		: moduleData['sequence'],
      'patterns'		: convertPatterns( moduleData['patterns'] ),
      'instruments'		: convertInstruments( moduleData['instruments'] )
    }
    
    writeOutputFile( outFile, convertedModule )

    logging.info( 'Successfully wrote converted module %s to %s' % tuple( [moduleData['name'], outFileName] ) )
    outputStatistics( statistics )
    
    inFile.close()
    outFile.close()

def outputStatistics( statistics ):

  outputTuple = tuple([
    statistics['samples'],
    statistics['minError'],
    statistics['maxError'],
    100.0 / statistics['samples'] * statistics['filter'][0],
    100.0 / statistics['samples'] * statistics['filter'][1],
    100.0 / statistics['samples'] * statistics['filter'][2],
    100.0 / statistics['samples'] * statistics['filter'][3],
    100.0 / statistics['samples'] * statistics['range'][0],
    100.0 / statistics['samples'] * statistics['range'][1],
    100.0 / statistics['samples'] * statistics['range'][2],
    100.0 / statistics['samples'] * statistics['range'][3],
    100.0 / statistics['samples'] * statistics['range'][4],
    100.0 / statistics['samples'] * statistics['range'][5],
    100.0 / statistics['samples'] * statistics['range'][6],
    100.0 / statistics['samples'] * statistics['range'][7],
    100.0 / statistics['samples'] * statistics['range'][8],
    100.0 / statistics['samples'] * statistics['range'][9],
    100.0 / statistics['samples'] * statistics['range'][10],
    100.0 / statistics['samples'] * statistics['range'][11],
    100.0 / statistics['samples'] * statistics['range'][12],
  ])
  
  logging.info( 'Converted %d BRR samples with error range %d-%d.\nFilter usage: 0:%d%% 1:%d%% 2:%d%% 3:%d%%\nRange usage: 0:%d%% 1:%d%% 2:%d%% 3:%d%% 4:%d%% 5:%d%% 6:%d%% 7:%d%% 8:%d%% 9:%d%% 10:%d%% 11:%d%% 12:%d%%' % outputTuple )

def getModuleLength( mod ):
  return ord( mod[950] )


def getModuleName( mod ):
  return mod[0:20]


def isValidModule( mod ):
  validModSignatures = [ 'M.K.', '4CHN']
  return mod[1080:1084] in validModSignatures

def writeOutputFile( outFile, mod ):
  writeChar( outFile, SPCMOD_SONG_LENGTH, mod['length'] )
  writeChar( outFile, SPCMOD_PATTERN_COUNT, mod['patternCount'] )
  writeSequence( outFile, mod['sequence'] )
  patternPointers = writePatterns( outFile, mod['patterns'] )
  writePatternPointers( outFile, patternPointers['patterns'] )
  samplePointers = writeSamples( outFile, patternPointers['end'], mod['instruments'] )
  writeInstruments( outFile, samplePointers, mod['instruments'] )
  


def writeChar( outFile, offset, data ):
  outFile.seek( offset )
  outFile.write( chr( data ) )


def writeSequence( outFile, sequence ):
  outFile.seek( SPCMOD_SEQUENCE )
  for pattern in sequence:
    outFile.write( chr( pattern ) )


def writePatterns( outFile, patterns ):
  patternPointer = []
  outFile.seek( SPCMOD_PATTERN_DATA )
  for pattern in patterns:
    patternPointer.append( outFile.tell() - SPCMOD_PATTERN_DATA )	#relative pointer to pattern
    for channel in pattern:
      if channel['valid']:
        outFile.write( chr( channel['instrument'] ) )
        outFile.write( chr( channel['period'] ) )
        outFile.write( chr( channel['effectCommand'] ) )
        outFile.write( chr( channel['effectData'] ) )
      else:
        outFile.write( chr( SPCMOD_EMPTY_CHANNEL ) )
  
  patternPointer.append( outFile.tell() - SPCMOD_PATTERN_DATA )	#relative pointer to end of last pattern. crude shit
  return {
    'patterns'	: patternPointer,
    'end'		: outFile.tell()
  }


def writePatternPointers( outFile, patternPointers ):
  outFile.seek( SPCMOD_PATTERN_POINTER )
  for pointer in patternPointers:
    outFile.write( chr( (pointer & 0xff00) >> 8 ) )
    outFile.write( chr( (pointer & 0xff) ) )

def writeSamples( outFile, sampleBufferPos, instruments ):
  outFile.seek( sampleBufferPos )
  
  samplePointer = []
  for instrument in instruments:
    samplePointer.append( {
      'start'		: outFile.tell(),
      'repeatStart' : outFile.tell() + ( instrument['repeatStart'] / BRR_BLOCK_SAMPLES * BRR_BLOCK_LENGTH )
    } )
    
    for i in range( len( instrument['samples'] ) ):
      sampleBlock = instrument['samples'][i]
      loop = 1 if instrument['repeatFlag'] else 0
      end = 1 if ( i == len( instrument['samples'] ) - 1 ) else 0
      header = ( sampleBlock['range'] << 4 ) | ( sampleBlock['filter'] << 2 ) | ( loop << 1 ) | end
      
      outFile.write( chr( header ) )
      for i in range( 8 ):
        outFile.write( chr( mergeBrrSample( i, sampleBlock['samples'] ) ) )
  return samplePointer


def mergeBrrSample( pos, samples ):
  return ( samples[pos*2] << 4 ) | samples[(pos*2)+1] 


def writeInstruments( outFile, samplePointers, instruments ):
  outFile.seek( SPCMOD_INSTRUMENT_DATA )
  for i in range(len(instruments)):
    outFile.write( chr( (samplePointers[i]['start'] & 0xff00) >> 8 ) )
    outFile.write( chr( (samplePointers[i]['start'] & 0xff) ) )
    outFile.write( chr( instruments[i]['finetune'] ) )
    outFile.write( chr( instruments[i]['volume'] ) )
    outFile.write( chr( (samplePointers[i]['repeatStart'] & 0xff00) >> 8 ) )
    outFile.write( chr( (samplePointers[i]['repeatStart'] & 0xff) ) )
    outFile.write( chr( 0 ) )
    outFile.write( chr( 0 ) )
    debugLog( 'wrote instrument %x start: %x, repeat: %x, length in samples: %x' % tuple( [i+1, samplePointers[i]['start'], samplePointers[i]['repeatStart'], len( instruments[i]['samples'] ) * 16  ] ) )
    

def convertInstruments( inputInstruments ):
  convertedInstruments = []
  for instrument in inputInstruments:
    convertedInstruments.append( convertInstrument( instrument ) )
  return convertedInstruments


def convertInstrument( inputInstrument ):
  multipliedInstrument = multiplyInstrumentResolution( inputInstrument, INSTR_RES_MULTI )
  paddedInstrument = padInstrumentSamples( multipliedInstrument )
  
  return {
    'finetune'		: paddedInstrument['finetune'],
    'volume'		: paddedInstrument['volume'],
    'repeatStart'	: paddedInstrument['repeatStart'],
    'repeatFlag'	: paddedInstrument['repeatFlag'],
    'samples'		: convertInstrumentSamples( paddedInstrument['samples'], paddedInstrument['repeatStart'], paddedInstrument['repeatFlag'] )
  }

def multiplyInstrumentResolution( inputInstrument, factor ):
  return {
    'finetune'		: inputInstrument['finetune'],
    'volume'		: inputInstrument['volume'],
    'repeatStart'	: inputInstrument['repeatStart'] * factor,
    'repeatLength'	: inputInstrument['repeatLength'] * factor,
    'samples'		: multiplySampleResolution( inputInstrument['samples'], factor )
  }


def multiplySampleResolution( samples, factor ):
  outputSamples = []
  for sample in samples:
    for i in range( factor ):
      outputSamples.append( sample )
  return outputSamples

def padInstrumentSamples( inputInstrument ):
  preLoopSamples = inputInstrument['samples'][:inputInstrument['repeatStart']]
  postLoopSamples = inputInstrument['samples'][inputInstrument['repeatStart']:]
  postLoopSamplesOrig = postLoopSamples

  repeatFlag = True if inputInstrument['repeatLength'] > 0 else False
  #debugLog( 'reading instrument, %x pre-loop samples, %x post-loop samples, %x total samples' % tuple( [len( preLoopSamples ), len( postLoopSamples ), len( inputInstrument['samples'] ) ] ) )
  #pad sample start - repeat start until multiple of 16
  while len( preLoopSamples ) % BRR_BLOCK_SAMPLES != 0:
    preLoopSamples.insert( 0, getEmptySample() )

  #prepend 16 samples to any sample to avoid click on note trigger
  for i in range(BRR_BLOCK_SAMPLES):
    preLoopSamples.insert( 0, getEmptySample() )

  #append 25 samples to one shot-instrument
  if not repeatFlag:
    for i in range(BRR_ONE_SHOT_EXTEND):
      postLoopSamples.append( getEmptySample() )

  #pop samples of big looping or one-shot samples until multiple of 16
  if len( postLoopSamples ) > SAMPLE_CUT_THRESHOLD or not repeatFlag:
    while len( postLoopSamples ) % BRR_BLOCK_SAMPLES != 0:
      postLoopSamples.pop()
  #multiply short looping samples until they are multiple of 16
  else:
    while len( postLoopSamples ) % BRR_BLOCK_SAMPLES != 0:
      postLoopSamples.extend( postLoopSamplesOrig )
  
  return {
    'finetune'		: inputInstrument['finetune'],
    'volume'		: inputInstrument['volume'],
    'repeatStart'	: len( preLoopSamples ),
    'repeatFlag'	: repeatFlag,
    'samples'		: groupSamples( preLoopSamples + postLoopSamples ) if len( inputInstrument['samples'] ) > BRR_BLOCK_SAMPLES else []
  }


def getEmptySample():
  return 0


#group samples into blocks of 16 sample each
def groupSamples( inputSamples ):
  groupedSamples = []
  while len( inputSamples ) > 0:
    sampleBlock = []
    for i in range( BRR_BLOCK_SAMPLES ):
      sampleBlock.append( inputSamples.pop( 0 ) )
    groupedSamples.append( sampleBlock )
  return groupedSamples


def convertInstrumentSamples( inputSamples, repeatStart, repeatFlag ):
  convertedSamples = []
  
  noFilterSamples = [ 0, 1, 2, repeatStart, repeatStart + 1, repeatStart + 2 ]
  
  i = 0
  while i < len( inputSamples ):
    sampleBlock = inputSamples[i]
    forceNoFilter = True #if i in noFilterSamples else False
    convertedSamples.append( convertSample( sampleBlock, forceNoFilter ) )
    i += 1
  return convertedSamples


def convertSample( inputSampleBlock, forceNoFilter ):
  optimumSample = {
    'blockError' : BRR_BLOCK_SAMPLES * 0xffff	#max possible error
  }
  globalSampleBuffer = {
    'last'			: 0,
    'beforeLast'	: 0
  }
  for rangeVal in range( BRR_MAX_RANGE_SHIFT ):
      for filterVal in range ( BRR_FILTERS ):
        currentFilter = filterVal if forceNoFilter == False else 0
        #currentFilter = 0
        sampleBlock = convertSampleBlock( inputSampleBlock, { 'filter' : currentFilter, 'range' : rangeVal } )

        if sampleBlock['blockError'] < optimumSample['blockError']:
          optimumSample = sampleBlock

  #debugLog(optimumSample, 'optimum sample')
  updateStatistics( optimumSample )
  
  globalSampleBuffer['last']		= optimumSample['simulatedSamples'].pop()	#selected optimum sample becomes last in buffer
  globalSampleBuffer['beforeLast']	= optimumSample['simulatedSamples'].pop()

  return {
    'filter'	: optimumSample['filter'],
    'range'		: optimumSample['range'],
    'samples'	: optimumSample['convertedCharSamples'],
  }


def convertSampleBlock( inputSampleBlock, config ):
  blockError = 0
  convertedSamples = []
  simulatedSamples = []
  convertedCharSamples = []
  
  for sample in inputSampleBlock:
    signedSample = unsigned16BitToSigned( sample )
    convertedSignedSample = convertSingleSample( signedSample, config )
    convertedCharSample = signedToUnsigned4Bit( convertedSignedSample )
    simulatedBrrSample = simulateBrrSample( convertedSignedSample, config )
    
    convertedSamples.append( convertedSignedSample )	
    simulatedSamples.append( simulatedBrrSample )
    convertedCharSamples.append( convertedCharSample )

    error = calculateBrrError( signedSample, simulatedBrrSample )
    blockError += error * error
    
    globalSampleBuffer['beforeLast']	= globalSampleBuffer['last']
    globalSampleBuffer['last']			= simulatedBrrSample
  
  return {
    'blockError'			: math.sqrt( blockError ),
    'convertedSamples'		: convertedSamples,
    'convertedCharSamples'	: convertedCharSamples,
    'simulatedSamples'		: simulatedSamples,
    'originalSamples'		: inputSampleBlock,
    'filter'				: config['filter'],
    'range'					: config['range'],
  }


def convertSingleSample( inputSample, config ):
  if inputSample < 0:
    return -( ( abs( inputSample ) >> config['range'] ) & 0x7 )
  else:
    return ( inputSample >> config['range'] ) & 0x7
  #return clampSignedSampleToRange( ( inputSample >> config['range'] ), 0x7 )


#restrict range of sample
def clampSignedSampleToRange( inputSample, limit ):
  return min( limit, max( -limit, inputSample ) )


def unsigned16BitToSigned( sample ):
  return sample if sample < 0x8000 else sample - 0x10000


def signedToUnsigned4Bit( sample ):
  return sample if sample >= 0 else ( abs( sample ) ^ 0xf ) + 1


def simulateBrrSample ( brrSample, config ):
  sample = brrSample
  sample <<= config['range']
  sample >>= 1
  brrFilterLUT = getBrrFilterLUT()
  sample += brrFilterLUT[config['filter']]()
  sample = clampSignedSampleToRange( sample, 0x7fff )
  sample <<= 1
  return sample


def calculateBrrError( inputSample, brrSample ):
  return max( inputSample, brrSample ) - min( inputSample, brrSample )


def getBrrFilterLUT():
  return {
    0	: applyNoFilter,
    1	: applyFilter1,
    2	: applyFilter2,
    3	: applyFilter3
  }  


def applyNoFilter():
  return 0


def applyFilter1():
  s = globalSampleBuffer['last'] >> 1
  s += (-globalSampleBuffer['last']) >> 5
  return s
# return globalSampleBuffer['last'] * 0.46875


def applyFilter2():
  s = globalSampleBuffer['last'];
  s -= globalSampleBuffer['beforeLast'] >> 1;
  s += globalSampleBuffer['beforeLast'] >> 5;
  s += (globalSampleBuffer['last'] * -3) >> 6;  
  return s
  #return globalSampleBuffer['last'] * 0.953125 - globalSampleBuffer['beforeLast'] * 0.46875


def applyFilter3():
  s = globalSampleBuffer['last'];
  s -= globalSampleBuffer['beforeLast'] >> 1;
  s += (globalSampleBuffer['last'] * -13) >> 7;
  s += ((globalSampleBuffer['beforeLast'] >> 1) * 3) >> 4;  
  return s
  #return globalSampleBuffer['last'] * 0.8984375 - globalSampleBuffer['beforeLast'] * 0.40625


def updateStatistics( optimumSample ):
  statistics['samples'] += 1
  statistics['filter'][optimumSample['filter']] += 1
  statistics['range'][optimumSample['range']] += 1
  statistics['maxError'] = max( statistics['maxError'], optimumSample['blockError'] )
  statistics['minError'] = min( statistics['minError'], optimumSample['blockError'] )
  return statistics


def convertPatterns( inputPatterns ):
  convertedPatterns = []
  
  for pattern in inputPatterns:
    convertedPatterns.append( convertPattern( pattern ) )
  return convertedPatterns


def convertPattern( pattern ):
  convertedPattern = []
  
  for row in pattern:
    for channel in row:
      convertedPattern.append( convertChannel( channel ) )
  return convertedPattern


def convertChannel( channel ):
  convertedPeriod = convertPeriod( channel['period'] )
  
  return {
    'instrument'	: channel['instrument'],
    'period'		: convertedPeriod if convertedPeriod else SPCMOD_INVALID_PERIOD,
    'effectCommand'	: channel['effectCommand'] if channel['effectCommand'] + channel['effectData'] > 0 else SPCMOD_INVALID_PERIOD,
    'effectData'	: channel['effectData'] if channel['effectCommand'] + channel['effectData'] > 0 else SPCMOD_INVALID_PERIOD,
    'valid'			: True
  } if convertedPeriod or channel['effectData'] > 0 or channel['effectCommand'] > 0 else {
    'valid'			: False
  }
  


def convertPeriod( inputPeriod ):
  periodLUT = getPeriodLUT()
  
  if not inputPeriod in periodLUT:
    if inputPeriod > 0:
      logging.info( 'input period %s is out of conversion range.' % inputPeriod )
    return False
  return 2 * ( periodLUT[inputPeriod] + ( MOD_PERIODS_PER_OCTAVE * ( INSTR_RES_MULTI - 1 ) ) )


def getModuleSampleBufferPosition( patternCount ):
  return ( ( patternCount + 1 ) * MOD_ROWS_PER_PATTERN * MOD_CHANNELS * 4 ) + 1084


def getModulePatternCount( sequence ):
  return max( sequence )


def getModulePlaySequence( mod ):
  sequence = []
  for char in mod[952:1080]:
    sequence.append( ord( char ) )
  return sequence


def getModulePatterns( mod, patternCount ):
  patterns = []

  i = 0
  while i <= patternCount:
    patterns.append( getModulePattern( mod, i ) )
    i += 1
  return patterns


def getModulePattern( mod, patternId ):
  rows = []
  
  patternData = mod[ ( patternId * MOD_ROWS_PER_PATTERN * MOD_CHANNELS * MOD_BYTES_PER_CHANNEL ) + 1084 : ( ( patternId + 1 ) * MOD_ROWS_PER_PATTERN * MOD_CHANNELS * MOD_BYTES_PER_CHANNEL ) + 1084 ]

  for i in range( MOD_ROWS_PER_PATTERN ):
    rows.append( getModulePatternRow( patternData, i ) )
  return rows


def getModulePatternRow( patternData, rowId ):
  channels = []

  channelData = patternData[ rowId * MOD_CHANNELS * MOD_BYTES_PER_CHANNEL : ( rowId + 1 ) * MOD_CHANNELS * MOD_BYTES_PER_CHANNEL ]

  i = 0
  while i < MOD_CHANNELS:
    channels.append( getModulePatternRowChannel( channelData, i ) )
    i += 1
  return channels


def getModulePatternRowChannel( channelData, channelId ):
  singleChannelData = channelData[ channelId * MOD_BYTES_PER_CHANNEL : ( channelId + 1 ) * MOD_BYTES_PER_CHANNEL ]
  return {
    'instrument'	: ( ord( singleChannelData[0] ) & 0xf0 ) | ( ( ord( singleChannelData[2] ) & 0xf0 ) >> 4 ),
    'period'		: ( ( ord( singleChannelData[0] ) & 0xf ) << 8 ) | ord( singleChannelData[1] ),
    'effectCommand'	: ord( singleChannelData[2] ) & 0xf,
    'effectData'	: ord( singleChannelData[3] )
  }


def getModuleInstruments( mod, currentSampleBufferPosition ):
  instruments = []
  instrumentData = mod[MOD_INSTRUMENT_DATA:MOD_INSTRUMENT_DATA + ( MOD_INSTRUMENT_DATA_LENGTH * MOD_INSTRUMENT_COUNT )]

  for i in range( MOD_INSTRUMENT_COUNT ):
    instruments.append( getModuleInstrument( i, instrumentData, mod, currentSampleBufferPosition ) )
    currentSampleBufferPosition += instruments[i]['length']

  return instruments


def getModuleInstrument( instrumentId, instrumentData, mod, sampleBufferPosition ):
  singleInstrument = instrumentData[ instrumentId * MOD_INSTRUMENT_DATA_LENGTH : ( instrumentId + 1 ) * MOD_INSTRUMENT_DATA_LENGTH ]
  instrument = {
    'name'			: singleInstrument[0:22],
    'start'			: sampleBufferPosition,
    'length'		: checkInstrumentLength( charWordToInt( singleInstrument[22:24] ) ),
    'finetune'		: ord( singleInstrument[24] ),
    'volume'		: ord( singleInstrument[25] ),
    'repeatStart'	: charWordToInt( singleInstrument[26:28] ),
    'repeatLength'	: checkInstrumentLength( charWordToInt( singleInstrument[28:30] ) )
  }

  instrument['samples'] = getInstrumentSamples(
    instrument['start'],
    instrument['length'],
    mod
  )
  
  #debugLog(instrument)  
  return instrument


def checkInstrumentLength( length ):
  return length if length >= BRR_BLOCK_SAMPLES else 0

def getInstrumentSamples( start, length, sampleData ):
  samples = []
  for char in sampleData[ start : start+length ]:
    samples.append( ( ord( char ) << 8 ) | ord( char ) )	#fetch 16bit samples with dither
    #samples.append( ord( char ) << 8 )	#fetch 16bit samples
  return samples


def charWordToInt( char ):
  return ( ord( char[1] ) + ( ord( char[0] ) << 8 ) ) * 2


def debugLog( data, message = '' ):
    logging.debug( message )
    debugLogRecursive( data, '' )

def debugLogExit( data, message = '' ):
    logging.debug( message )
    debugLogRecursive( data, '' )
    sys.exit()

def debugLogRecursive( data, nestStr ):
  nestStr += ' '
  if type( data ) is dict:
    logging.debug( '%s dict{' % nestStr )	
    for k, v in data.iteritems():
      logging.debug( ' %s %s:' % tuple( [nestStr, k] ) )
      debugLogRecursive( v, nestStr )
    logging.debug( '%s }' % nestStr )

  elif type( data ) is list:
    logging.debug( '%s list[' % nestStr )
    for v in data:
      debugLogRecursive( v, nestStr )
    logging.debug( '%s ]' % nestStr )

  else:
    if type( data ).__name__ == 'int':
      logging.debug( ' %s %x' % tuple( [nestStr, data] ) )
    else:
      logging.debug( ' %s %s' % tuple( [nestStr, data] ) )

#ugly lookup table, hopefully replaceable by something more elegant
def getPeriodLUT():
  return {
    0x0358 : 0,	#oct 1, C
    0x0328 : 1,
    0x02FA : 2,
    0x02D0 : 3,
    0x02A6 : 4,
    0x0280 : 5,
    0x025C : 6,
    0x023A : 7,
    0x021A : 8,
    0x01FC : 9,
    0x01E0 : 10,
    0x01C5 : 11,
    0x01AC : 12, #oct 2, C
    0x0194 : 13,
    0x017D : 14,
    0x0168 : 15,
    0x0153 : 16,
    0x0140 : 17,
    0x012E : 18,
    0x011D : 19,
    0x010D : 20,
    0x00FE : 21,
    0x00F0 : 22,
    0x00E2 : 23,
    0x00D6 : 24, #oct 3, C
    0x00CA : 25,
    0x00BE : 26,
    0x00B4 : 27,
    0x00AA : 28,
    0x00A0 : 29,
    0x0097 : 30,
    0x008F : 31,
    0x0087 : 32,
    0x007F : 33,
    0x0078 : 34,
    0x0071 : 35,
    0x006B : 36,
    0x0065 : 37,
    0x005F : 38,
    0x005A : 39,
    0x0055 : 40,
    0x0050 : 41,
    0x004B : 42,
    0x0047 : 43,
    0x0043 : 44,
    0x003F : 45,
    0x003C : 46,
    0x0038 : 47,
    0x0035 : 48,
    0x0032 : 49,
    0x002F : 50,
    0x002D : 51,
    0x002A : 52,
    0x0028 : 53,
    0x0025 : 54,
    0x0023 : 55,
    0x0021 : 56,
    0x001F : 57,
    0x001e : 58,
    0x001c : 59
  }


if __name__ == "__main__":
    main()

#	for arg in sys.argv:
#		logging.info(' %s' % arg)

#        try:
#            Image.open(infile).save(outfile)
#        except IOError:
#            print "Cannot convert", infile
#file = open(filename+'.'+'%03d' % framecounter, 'wb')
#len(polys)
#ord(): get int from char(file byte)
#chr(): get 
