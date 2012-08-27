#!/usr/bin/env python

__author__ = "Matthias Nagler <matt@dforce.de>"
__url__ = ("dforce3000", "dforce3000.de")
__version__ = "0.1"

'''
rename folders from snesmusic rsn to actual game name
'''
import os
import sys
import logging

logging.basicConfig( level=logging.INFO, format='%(message)s')

options = {}


INFINITY = 1e300000
HEADER_SIZE = 0x20
CHAPTER_SIZE = 0x4
POINTER_SIZE = 0x4
FRAME_SIZE = 0x6
MAX_CHAPTERS = 0xff

TILES = 0
TILEMAP = 1
PALETTE = 2

class UserOptions():
  def __init__( self ):
	for option in defaultOptions:
	  self.setOption(option)


def main():
  options = UserOptions( sys.argv, {
	'bpp' 		: {
	  'value'			: 4,
	  'type'			: 'int',
	  'max'			: 8,
	  'min'			: 1
	  },
	'infilebase'		: {
	  'value'			: '',
	  'type'			: 'str'
	  },
	'outfile'		: {
	  'value'			: '',
	  'type'			: 'str'
	  },
	'title'		: {
	  'value'			: '',
	  'type'			: 'str'
	  },
	'fps' 		: {
	  'value'			: 24,
	  'type'			: 'int',
	  'max'			: 60,
	  'min'			: 1
	  },	
  })

  if not os.path.exists(options.get('infilebase')):
	logging.error( 'Chapter base-folder "%s" is nonexistant.' % options.get('infilebase') )
	sys.exit(1)

  chapters = sorted([Chapter(chapterDir, options) for root, dirs, names in os.walk(options.get('infilebase')) for chapterDir in dirs], key=lambda chapter: chapter.id)

  if not len(chapters) > 0:
	logging.error( 'No chapter folders are present inside specified chapter base folder %s.' % options.get('infilebase'))
	sys.exit(1)

  if len(chapters) > MAX_CHAPTERS:
	logging.error( 'Too many chapters, maximum of %s are allowed, %s are present.' % (MAX_CHAPTERS, len(chapters)))
	sys.exit(1)

  outFile = getOutFile(options.get('outfile'))
  outFile.write("S-MSU1")
  outFile.write("%-21s" % options.get('title').upper())
  if (options.get('bpp') == 2):
	colorDepth = 4
  elif (options.get('bpp') == 4):
	colorDepth = 5
  elif (options.get('bpp') == 8):
	colorDepth = 6
  else:
	  logging.error( 'Invalid color depth %s.' % options.get('bpp') )
	  sys.exit(1)
	  
  outFile.write(chr(colorDepth))
  outFile.write(chr(options.get('fps')))
	  
  outFile.write(chr(len(chapters) & 0xff))
  
  #pad header
  [outFile.write(chr(0)) for i in range(HEADER_SIZE - outFile.tell())]

  scenePointerOffset = HEADER_SIZE
  sceneOffset = scenePointerOffset + (len(chapters) * POINTER_SIZE)
  frameOffset = sceneOffset
  for chapter in chapters:
	frameOffset += CHAPTER_SIZE + (len(chapter.frames) * POINTER_SIZE)

  #write chapter pointer blocks
  outFile.seek(scenePointerOffset)
  pointer = sceneOffset
  for chapter in chapters:
	writePointer(outFile, pointer)
	pointer += CHAPTER_SIZE + (len(chapter.frames) * POINTER_SIZE)


  #write chapters
  outFile.seek(sceneOffset)
  pointer = frameOffset
  for chapter in chapters:
	logging.debug('Now writing scene %02d (%s) at offset 0x%08x.' % (chapter.id, chapter.name, outFile.tell()))
	#write id/audio track #
	outFile.write(chr(chapter.id & 0xff))
	#write framecount
	outFile.write(chr(len(chapter.frames) & 0xff))
	outFile.write(chr((len(chapter.frames) & 0xff00) >> 8))
	outFile.write(chr((len(chapter.frames) & 0xff0000) >> 16))
	#frame pointers to frames in chapter
	for frame in chapter.frames:
	  writePointer(outFile, pointer)
	  pointer += FRAME_SIZE + frame.length

	#write audio file to build directory
	chapterAudioFileName = "%s-%d.pcm" % (os.path.splitext(options.get('outfile'))[0], chapter.id)
	logging.debug('Now writing audio file %s of scene %02d (%s).' % (chapterAudioFileName, chapter.id, chapter.name))
	audioOutFile = getOutFile(chapterAudioFileName)
	[audioOutFile.write(byte) for byte in chapter.audio]
	


  #write frames
  outFile.seek(frameOffset)
  for chapter in chapters:
	frameId = 0
	for frame in chapter.frames:
	  logging.debug('Now writing frame %s of scene %02d (%s) at offset 0x%08x.' % (frame.name, chapter.id, chapter.name, outFile.tell()))
	  lengthHeader = ((len(frame.tilemap) / 2) & 0x7ff) | (((len(frame.tiles) >> colorDepth) & 0x7ff) << 11) | (((len(frame.palette) / 2) & 0xff) << 22)
	  outFile.write(chr(frameId & 0xff))
	  outFile.write(chr((frameId & 0xff00) >> 8))
	  outFile.write(chr(lengthHeader & 0xff))
	  outFile.write(chr((lengthHeader & 0xff00) >> 8))
	  outFile.write(chr((lengthHeader & 0xff0000) >> 16))
	  outFile.write(chr((lengthHeader & 0xff000000) >> 24))	
	  [outFile.write(byte) for byte in frame.tilemap]
	  [outFile.write(byte) for byte in frame.tiles]
	  [outFile.write(byte) for byte in frame.palette]
	  frameId += 1

  outFile.close()
  logging.info('Successfully wrote msu1 data file %s, processed %s chapters containing %s frames.' % (options.get('outfile'), len(chapters), len([frame for chapter in chapters for frame in chapter.frames])))


def writePointer(fileHandle, pointer):
  fileHandle.write(chr(pointer & 0xff))
  fileHandle.write(chr((pointer & 0xff00) >> 8))
  fileHandle.write(chr((pointer & 0xff0000) >> 16))
  fileHandle.write(chr((pointer & 0xff000000) >> 24))

class Chapter():
  def __init__(self, chapterDir, options):

	self.name = chapterDir
	self.path = '%s/%s/' % (options.get('infilebase'), chapterDir)
	  
	if not os.path.exists(self.path):
	  logging.error( 'Chapter folder "%s" is nonexistant.' % self.path )
	  sys.exit(1)

	#get chapter id file
	idFiles = [idFile for root, dirs, files in os.walk(self.path) for idFile in sorted(files) if idFile.find("chapter.id") >= 0]
	if not 1 == len(idFiles):
	  logging.error( 'Chapter folder %s must contain exactly one id file, but actually contains %s.' % (chapterDir, len(idFiles)))
	  sys.exit(1)

	idFile = idFiles.pop()
	
	try:
	  self.id = int(idFile[11:])
	except ValueError:
	  logging.error( 'Invalid chapter id in id-file %s.' % idFile )
	  sys.exit(1)

	self.frames = [Frame(os.path.splitext(frameBaseFile)[0], self.path, options) for root, dirs, files in os.walk(self.path) for frameBaseFile in sorted(files) if frameBaseFile.find("gfx_video.tiles") >= 0]

	#this is a hack that pads out each chapter with a couple of frames to make up for timing differences
	self.frames.append(self.frames[-1])
	self.frames.append(self.frames[-1])
	#get chapter audio file
	audioFiles = [audio for root, dirs, files in os.walk(self.path) for audio in sorted(files) if audio.find("sfx_video.pcm") >= 0]
	if not 1 == len(audioFiles):
	  logging.error( 'Chapter folder %s must contain exactly one msu1 pcm audio file, but actually contains %s.' % (chapterDir, len(audioFiles)))
	  sys.exit(1)

	self.audio = getInFile('%s%s' % (self.path, audioFiles.pop())).read()
  

class Frame():
  def __init__(self, frameFileBase, path, options):
	self.name = frameFileBase
	tempFile = getInFile('%s%s.tiles' % (path, frameFileBase))
	self.tiles = tempFile.read()
	tempFile.close()
	tempFile = getInFile('%s%s.tilemap' % (path, frameFileBase))
	self.tilemap = tempFile.read()
	tempFile.close()
	tempFile = getInFile('%s%s.palette' % (path, frameFileBase))
	self.palette = tempFile.read()
	tempFile.close()
	self.length = len(self.tiles) + len(self.tilemap) + len(self.palette)



def getOutFile( fileName ):
  try:
	outFile = open( fileName, 'wb' )
  except IOError:
	logging.error( 'unable to access required output-file %s' % fileName )
	sys.exit(1)
  return outFile


def getInFile( fileName ):
  try:
	inFile = open( fileName, 'rb' )
  except IOError:
	logging.error( 'unable to access required input-file %s' % fileName )
	sys.exit(1)
  return inFile


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

