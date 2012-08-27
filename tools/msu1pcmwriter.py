#!/usr/bin/env python

__author__ = "Matthias Nagler <matt@dforce.de>"
__url__ = ("dforce3000", "dforce3000.de")
__version__ = "0.1"

'''
justs verifies input wave files are in the right format and slaps on the the header


command line options:
-infile	
-outfile
-loopstart

msu1 pcm file format:
  [header{(8 bytes)
	4 bytes magic: "MSU1"
	4 bytes loop point
	? bytes 44.1 kilohertz, 16-bit stereo uncompressed unsigned PCM files in little-endian order, left channel first	
  }]
'''

import os
import sys
import math
import time
import wave
import logging

'''
debugfile = open('debug.log', 'wb')
debugfile.close()
logging.basicConfig( filename='debug.log',
					level=logging.DEBUG,
					format='%(message)s')
'''

logging.basicConfig( level=logging.INFO, format='%(message)s')

options = {}


INFINITY = 1e300000
CHANNEL_NUMBER = 2
SAMPLE_WIDTH = 16 / 8
SAMPLE_RATE = 44100
COMPRESSION_TYPE = 'NONE'
HEADER_MAGIC = 'MSU1'
RIFF_PCM_DATA = 44


class UserOptions():
  def __init__( self ):
	for option in defaultOptions:
	  self.setOption(option)


def main():
  options = UserOptions( sys.argv, {
	'loopstart' 		: {
	  'value'			: 0,
	  'type'			: 'int',
	  'max'			: 0xffffffff,
	  'min'			: 0
	  },
	'infile'		: {
	  'value'			: '',
	  'type'			: 'str'
	  },
	'outfile'		: {
	  'value'			: '',
	  'type'			: 'str'
	  },
  })


  try:
	inputFile = wave.open(options.get('infile'), 'rb')
  except IOError:
	logging.error( 'Unable to access input file "%s".' % options.get('infile') )
	sys.exit(1)

  if not CHANNEL_NUMBER == inputFile.getnchannels():
	logging.error( 'Error, input file must have %s channels, but has %s.' % (CHANNEL_NUMBER, inputFile.getnchannels()) )
	sys.exit(1)

  if not SAMPLE_WIDTH == inputFile.getsampwidth():
	logging.error( 'Error, input file sample size must be %s Bit, but is %s Bit.' % (SAMPLE_WIDTH * 8, inputFile.getsampwidth() * 8) )
	sys.exit(1)

  if not SAMPLE_RATE == inputFile.getframerate():
	logging.error( 'Error, input file sample rate must be %s Hz, but is %s Hz.' % (SAMPLE_RATE, inputFile.getframerate()) )
	sys.exit(1)

  if not COMPRESSION_TYPE == inputFile.getcomptype():
	logging.error( 'Error, input file compression must be of type %s, but is of type %s.' % (COMPRESSION_TYPE, inputFile.getcomptype()) )
	sys.exit(1)


  try:
	outFile = open( options.get('outfile'), 'wb' )
  except IOError:
	logging.error( 'Unable to access output file %s' % options.get('outfile') )
	sys.exit(1)

  try:
	inputFile = open(options.get('infile'), 'rb')
  except IOError:
	logging.error( 'Unable to access input file "%s".' % options.get('infile') )
	sys.exit(1)

  inputFile.seek(RIFF_PCM_DATA)
  outFile.seek(0)
  outFile.write(HEADER_MAGIC)
  outFile.write(chr(options.get('loopstart') & 0xff))
  outFile.write(chr((options.get('loopstart') & 0xff00) >> 8))
  outFile.write(chr((options.get('loopstart') & 0xff0000) >> 16))
  outFile.write(chr((options.get('loopstart') & 0xff000000) >> 24))	
  [outFile.write(byte) for byte in inputFile.read()]
  
  logging.info('Successfully wrote msu1 pcm audio file %s.' % options.get('outfile'))


class UserOptions():
  def __init__( self, args, defaults ):
	self.__options = self.__parseUserArguments(args, defaults)

  def get( self, option ):
	if option in self.__options:
	  return self.__options[option]['value']
	else:
	  logging.error( 'Invalid option %s requested.' % option )
	  sys.exit(1)

  def manualSet( self, option, value ):
	self.__options[option]['value'] = value


  def __parseUserArguments( self, args, defaults ):
	options = defaults
	  
	for i in range( len( args ) ):
	  if args[i][1:] in defaults:
		options[args[i][1:]]['value'] = args[i+1]
	return self.__sanitizeOptions( options )


  def __sanitizeOptions( self, options ):
	for optionName, optionValue in options.iteritems():
	  sanitizerLUT = self.__getSanitizerLUT()
	  options[optionName] = sanitizerLUT[optionValue['type']]( optionName, optionValue )	
	return options


  def __sanitizeInt( self, optionName, optionValue ):
	if type( optionValue['value'] ) is not int:
	  try:
		optionValue['value'] = int( optionValue['value'], 10 )
	  except ( TypeError, ValueError ):
		logging.error( 'Invalid argument %s for option -%s.' % ( optionValue['value'], optionName ) )
		sys.exit(1)
	if optionValue['value'] < optionValue['min'] or optionValue['value'] > optionValue['max']:
		logging.error( 'Argument %s for option -%s is out of allowed range %s - %s.' % ( optionValue['value'], optionName, optionValue['min'], optionValue['max'] ) )
		sys.exit(1)
	return optionValue

  def __sanitizeFloat( self, optionName, optionValue ):
	if type( optionValue['value'] ) is not float:
	  try:
		optionValue['value'] = float( optionValue['value'] )
	  except ( TypeError, ValueError ):
		logging.error( 'Invalid argument %s for option -%s.' % ( optionValue['value'], optionName ) )
		sys.exit(1)
	if optionValue['value'] < optionValue['min'] or optionValue['value'] > optionValue['max']:
		logging.error( 'Argument %s for option -%s is out of allowed range %s - %s.' % ( optionValue['value'], optionName, optionValue['min'], optionValue['max'] ) )
		sys.exit(1)
	return optionValue

  def __sanitizeHex( self, optionName, optionValue ):
	if type( optionValue['value'] ) is not int:
	  try:
		optionValue['value'] = int( optionValue['value'], 16 )
	  except ( TypeError, ValueError ):
		logging.error( 'Invalid argument %s for option -%s.' % ( optionValue['value'], optionName ) )
		sys.exit(1)
	if optionValue['value'] < optionValue['min'] or optionValue['value'] > optionValue['max']:
		logging.error( 'Argument %s for option -%s is out of allowed range %s - %s.' % ( optionValue['value'], optionName, optionValue['min'], optionValue['max'] ) )
		sys.exit(1)
	return optionValue
	
	
  def __sanitizeStr( self, optionName, optionValue ):
	if len( optionValue ) < 1:
		logging.error( 'Argument %s for option -%s is invalid.' % ( optionValue['value'], optionName ) )
		sys.exit(1)
	return optionValue


  def __sanitizeBool( self, optionName, optionValue ):
	if type( optionValue['value'] ) is str:
	  if optionValue['value'] not in ( 'on', 'off' ):
		logging.error( 'Argument %s for option -%s is invalid. Only on and off are allowed.' % ( optionValue['value'], optionName ) )
		sys.exit(1)
	  optionValue['value'] = True if optionValue['value'] == 'on' else False
	return optionValue
	
	
  def __getSanitizerLUT(self):
	return {
	  'int'	: self.__sanitizeInt,
	  'float'	: self.__sanitizeFloat,
	  'hex'	: self.__sanitizeHex,
	  'str'	: self.__sanitizeStr,
	  'bool'	: self.__sanitizeBool
	}    



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
	if type( data ) is int:
	  logging.debug( ' %s 0x%x %s ' % ( nestStr, data, type( data ) ) )
	else:
	  logging.debug( ' %s "%s" %s' % ( nestStr, data, type( data ) ) )

if __name__ == "__main__":
	main()

