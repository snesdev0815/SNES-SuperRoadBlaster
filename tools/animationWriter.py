#!/usr/bin/env python

__author__ = "Matthias Nagler <matt@dforce.de>"
__url__ = ("dforce3000", "dforce3000.de")
__version__ = "0.1"

'''
takes input graphics files(usually png), converts and packs them into animation file
first file determines palette to use
nice2have:
  -calculate required palettes, insert new palettes as needed
	-start at first palette, keep in buffer, save there
	-if buffer satisfies subsequent frame, use buffer there aswell. else replace buffer
	
  -somehow decide between frame tile uploads and packing all tiles into one tileset

command line options:
-infolder	input folder containing all animation frames, name-sorted
-outfile	output animation file

outfile format:
[sprite_animation{
  [header(8bytes){
	2 bytes : "SP", header magic
	2 bytes : max tile-size(bytes) in animation(for vram/sprite allocation)
	2 bytes : max palette-size(bytes) in animation(for cgram)
	2 bytes : frames in animation
  }],
  [pointer{
	2 bytes : relative pointer to individual sprite frame
  }]
  [sprite_frame{
  [header(6bytes){
	2 bytes : tilesize(bytes): if 0, no tiles present(use previous)
	2 bytes : spritemapsize(byte)
	2 bytes : palettesize(byte): if 0, no tiles present(use previous)
  }],
  [tiles]
  [spritemap]
  [palette]
  }]
}]  
'''

import os
import sys
import math
import time
import userOptions
import gracon
import logging
'''
debugfile = open('debug.log', 'wb')
debugfile.close()
logging.basicConfig( filename='debug.log',
					level=logging.DEBUG,
					format='%(message)s')
'''

logging.basicConfig( level=logging.DEBUG, format='%(message)s')

options = {}


INFINITY = 1e300000
HEADER_MAGIC = 'SP'
HEADER_SIZE = 9
FRAME_HEADER_SIZE = 6
ALLOWED_FRAME_FILETYPES = ('.png', '.gif', '.bmp')


def main():
  options = userOptions.Options( sys.argv, {
	'palettes' 		: {
	  'value'			: 1,
	  'type'			: 'int',
	  'max'			: 8,
	  'min'			: 0
	  },
	'transcol'	: {
	  'value'			: 0x7c1f,
	  'type'			: 'hex',
	  'max'			: 0x7fff,
	  'min'			: 0x0
	  },	  
	'infolder'		: {
	  'value'			: '',
	  'type'			: 'str'
	  },
	'outfile'		: {
	  'value'			: '',
	  'type'			: 'str'
	  },
	'refpalette'		: {
	  'value'			: '',
	  'type'			: 'str'
	  },
	'tilesizex'	: {
	  'value'			: 8,
	  'type'			: 'int',
	  'max'			: 16,
	  'min'			: 8
	  },
	'tilesizey'	: {
	  'value'			: 8,
	  'type'			: 'int',
	  'max'			: 16,
	  'min'			: 8
	  },
	'optimize'	: {
	  'value'			: True,
	  'type'			: 'bool'
	  },
    'directcolor'  : {
      'value'           : False,
      'type'            : 'bool'
      },      
	'tilethreshold'	: {
	  'value'			: 0,
	  'type'			: 'int',
	  'max'			: 0xffff,
	  'min'			: 0
	  },
    'maxtiles' : {
      'value'           : 0x3ff,
      'type'            : 'int',
      'max'         : 0x3ff,
      'min'         : 0
      },      	  
	'bpp' 		: {
	  'value'			: 4,
	  'type'			: 'int',
	  'max'			: 8,
	  'min'			: 1
	  },
	'mode'		: {
	  'value'			: 'bg',
	  'type'			: 'str'
	  },
	'resolutionx'	: {
	  'value'			: 256,
	  'type'			: 'int',
	  'max'			: 0xffff,
	  'min'			: 1
	  },	  
	'resolutiony'	: {
	  'value'			: 224,
	  'type'			: 'int',
	  'max'			: 0xffff,
	  'min'			: 1
	  },	  
  })

  if not os.path.exists(options.get('infolder')):
	logging.error( 'Error, input folder "%s" is nonexistant.' % options.get('infolder') )
	sys.exit(1)

  '''
  options.manualSet('tilesizex', 8)
  options.manualSet('tilesizey', 8)
  options.manualSet('bpp', 4)
  options.manualSet('mode', 'sprite')
  '''

  #tileFrames = sorted([gracon.parseTiles(gracon.getInputImage(options, "%s/%s" % (options.get('infolder'), frame)), options) for root, dirs, names in os.walk(options.get('infolder')) for frame in names if os.path.splitext(frame)[1] in ALLOWED_FRAME_FILETYPES], key=lambda frame: frame)
  tileFiles = [frame for root, dirs, names in os.walk(options.get('infolder')) for frame in names if os.path.splitext(frame)[1] in ALLOWED_FRAME_FILETYPES]
  tileFiles.sort()
  tileFrames = [gracon.parseTiles(gracon.getInputImage(options, "%s/%s" % (options.get('infolder'), frame)), options) for frame in tileFiles]

  if not 0 < len(tileFrames):
	logging.error( 'Error, input folder "%s" does not contain any parseable frame image files.' % options.get('infolder') )
	sys.exit(1)
	
  palette = gracon.parseGlobalPalettes( tileFrames[0], options )
 
  tileFrames = [gracon.augmentOutIds(gracon.optimizeTiles(gracon.palettizeTiles(frame, palette), options)) for frame in tileFrames]
  
  tileMapGetter = gracon.getSpriteTileMapStream if options.get('mode') == 'sprite' else gracon.getBgTileMapStream
  
  palette = gracon.augmentOutIds(palette)
  frames = [(gracon.getTileWriteStream(tileFrame, options), tileMapGetter(tileFrame, palette, options), gracon.getPaletteWriteStream([], options)) for tileFrame in tileFrames]

  #append palette to first
  if not options.get('directcolor'):
    frames[0] = (gracon.getTileWriteStream(tileFrames[0], options), tileMapGetter(tileFrames[0], palette, options), gracon.getPaletteWriteStream(palette, options))

  #collect some information about frames
  maxTileLength = 0
  maxPaletteLength = 0
  framecount = len(tileFrames)
  currentFramePointer = 0
  framePointers = []

  for frame in frames:
	framePointers.append(currentFramePointer)
	currentFramePointer += FRAME_HEADER_SIZE + len(frame[0]) + len(frame[1]) + len(frame[2])
	maxTileLength = len(frame[0]) if maxTileLength < len(frame[0]) else maxTileLength
	maxPaletteLength = len(frame[2]) if maxPaletteLength < len(frame[2]) else maxPaletteLength

  try:
	outFile = open( options.get('outfile'), 'wb' )
  except IOError:
	logging.error( 'unable to access required output-file %s' % options.get('outfile') )
	sys.exit(1)

  #write header
  outFile.write(HEADER_MAGIC)

  outFile.write(chr(maxTileLength & 0xff))
  outFile.write(chr((maxTileLength & 0xff00) >> 8 ))

  outFile.write(chr(maxPaletteLength & 0xff))
  outFile.write(chr((maxPaletteLength & 0xff00) >> 8 ))

  outFile.write(chr(framecount & 0xff))
  outFile.write(chr((framecount & 0xff00) >> 8 ))
  
  outFile.write(chr(int(options.get('bpp')/2) & 0xff))

  #write framepointerlist
  outFile.seek(HEADER_SIZE)
  for framePointer in framePointers:
	framePointer += HEADER_SIZE + len(framePointers)*2
	outFile.write(chr(framePointer & 0xff))
	outFile.write(chr((framePointer & 0xff00) >> 8 ))

  #write frames
  for frame in frames:
	#write frame header
	outFile.write(chr(len(frame[0]) & 0xff))
	outFile.write(chr((len(frame[0]) & 0xff00) >> 8 ))

	outFile.write(chr(len(frame[1]) & 0xff))
	outFile.write(chr((len(frame[1]) & 0xff00) >> 8 ))

	outFile.write(chr(len(frame[2]) & 0xff))
	outFile.write(chr((len(frame[2]) & 0xff00) >> 8 ))

	#write tiles, tilemap, palette
	[outFile.write(byte) for block in frame for byte in block]
	

  logging.info('Successfully wrote animation file %s.' % options.get('outfile'))


def debugLog( data, message = '' ):
	logging.info( message )
	debugLogRecursive( data, '' )


def debugLogExit( data, message = '' ):
	logging.info( message )
	debugLogRecursive( data, '' )
	sys.exit()


def debugLogRecursive( data, nestStr ):
  nestStr += ' '
  if type( data ) is dict:
	logging.info( '%s dict{' % nestStr )	
	for k, v in data.iteritems():
	  logging.info( ' %s %s:' % tuple( [nestStr, k] ) )
	  debugLogRecursive( v, nestStr )
	logging.info( '%s }' % nestStr )

  elif type( data ) is list:
	logging.info( '%s list[' % nestStr )
	for v in data:
	  debugLogRecursive( v, nestStr )
	logging.info( '%s ]' % nestStr )

  else:
	if type( data ) is int:
	  logging.info( ' %s 0x%x %s ' % ( nestStr, data, type( data ) ) )
	else:
	  logging.info( ' %s "%s" %s' % ( nestStr, data, type( data ) ) )
	  
if __name__ == "__main__":
	main()

