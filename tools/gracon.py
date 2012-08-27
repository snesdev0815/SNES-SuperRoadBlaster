#!/usr/bin/env python

__author__ = "Matthias Nagler <matt@dforce.de>"
__url__ = ("dforce3000", "dforce3000.de")
__version__ = "0.1"

'''
optimizations:
-flatten tile dict
  tile['data']
  
-flatten pixel arrays
  tile['data']['pixel']
  tile['data']['indexedPixel']
  

'''

'''
todo:
-check if images spanning multiple tilemaps have their tilemaps selected properly. probably not.
-have usage string if no parameter supplied or if parameter of unknown type found
'''

'''
convert graphics to snes bitplane format

options:
-bpp [1/2/4/8] (color depth mode, default: 4bpp)
-palnum [1-8] (maximum amount of palettes to allow, default: 1)
-mode [sprite|bg] (bg mode outputs tilemap, sprite mode outputs relative tilemap for 8x8 tiles)
-optimize [on|off] (don't rearrange tiles & don't output tilemap, default: on)
-transcol 0x[15bit transparent color] (every pixel having this color AFTER reducing image colordepth to snes 15bit format will be considered transparent. format: -bbbbbgg gggrrrrr default: 0x7C1F (pink))
-tilethreshold [int] (total difference in pixel color acceptable for two tiles to be considered the same. Cranking this value up potentially results in fewer tiles used in the converted image. this is meant to help identify parts of the image that may be optimized. default: 0)
-verify [on|off] (additionaly output converted image in png format(useful to verify that converted image looks fine)

possible input formats are: all supported by python Image module (png, gif, etc.)
input image alpha channel or transparency(gif/png) is dismissed completely. Relevant to transparent color of converted image is option -transcol" and nothing else.
image size will be padded to a multiple of tilesize and padded parts are filled with transparent color(palette color index 0).

format sprite tilemap (spritetilemap):
  x/y-offset relative to upper left corner of source image
  byte	0			1			2		3
		  cccccccc	vhopppcc	x-off	y-off
target format sprite tilemap:
  byte	0			1			2		3
		  x-off   y-off cccccccc	vhoopppN

  byte OBJ*4+0: xxxxxxxx
  byte OBJ*4+1: yyyyyyyy
  byte OBJ*4+2: cccccccc
  byte OBJ*4+3: vhoopppN

format bg tilemap:
  byte	0			1
		  cccccccc	vhopppcc
		  
directcolor mode:


'''

import os
import sys
import math
import time
import logging
import Image
import ImageDraw
import ImageFont
import userOptions

'''
debugfile = open('debug.log', 'wb')
debugfile.close()
logging.basicConfig( filename='debug.log',
					level=logging.DEBUG,
					format='%(message)s')
'''

logging.basicConfig( level=logging.INFO, format='%(message)s')


MAX_COLOR_COUNT = 256
INFINITY = 1e300000
BG_TILEMAP_SIZE = 32
LOOKBACK_TILES = 128
EMPTY_COLOR = 0



def main():
  options = userOptions.Options( sys.argv, {
	'bpp' 		: {
	  'value'			: 4,
	  'type'			: 'int',
	  'max'			: 8,
	  'min'			: 1
	  },
	'palettes'		: {
	  'value'			: 1,
	  'type'			: 'int',
	  'max'			: 8,
	  'min'			: 1
	  },
	'mode'		: {
	  'value'			: 'bg',
	  'type'			: 'str'
	  },
	'optimize'	: {
	  'value'			: True,
	  'type'			: 'bool'
	  },
    'directcolor'  : {
      'value'           : False,
      'type'            : 'bool'
      },	  
	'transcol'	: {
	  'value'			: 0x7c1f,
	  'type'			: 'hex',
	  'max'			: 0x7fff,
	  'min'			: 0x0
	  },
	'tilethreshold'	: {
	  'value'			: 1,
	  'type'			: 'int',
	  'max'			: 0xffff,
	  'min'			: 0
	  },	
	'verify'		: {
	  'value'			: False,
	  'type'			: 'bool'
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
    'maxtiles' : {
      'value'           : 0x3ff,
      'type'            : 'int',
      'max'         : 0x3ff,
      'min'         : 0
      },	  
	'refpalette'		: {
	  'value'			: '',
	  'type'			: 'str'
	  },
	'infile'		: {
	  'value'			: '',
	  'type'			: 'str'
	  },
	'outfilebase'		: {
	  'value'			: '',
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
  t0 = time.clock()

  if options.get('directcolor'):
    options.set('bpp', 8)
    options.set('palettes', 1)
  
  if not options.get('outfilebase'):
    options.set('outfilebase', options.get('infile'))
    
  inputImage = getInputImage( options, options.get('infile'))  
  tiles = parseTiles(inputImage, options)
  optimizedPalette = parseGlobalPalettes( tiles, options )
  palettizedTiles = palettizeTiles( tiles, optimizedPalette )

  #stupid hack that ensures certain amount of tiles are never exceeded for any given picture
  if options.get('optimize'):
    optimizedTiles = optimizeTiles( palettizedTiles, options )
    while len([tile for tile in optimizedTiles if tile['refId'] == None]) > options.get('maxtiles'):
      options.set('tilethreshold', options.get('tilethreshold') + 3)
      logging.info('maxtiles %s exceed, running again with threshold %s.' % (options.get('maxtiles'), options.get('tilethreshold')))
      optimizedTiles = optimizeTiles( palettizedTiles, options )
  else:
    optimizedTiles = palettizedTiles
    
  #optimizedTiles = optimizeTiles( palettizedTiles, options ) if options.get('optimize') else palettizedTiles
  
  #debugLogTileStatus(optimizedTiles)
  
  writeOutputFiles(optimizedTiles, optimizedPalette, inputImage, options)

  stats = Statistics(optimizedTiles, optimizedPalette, t0)
  logging.info('conversion complete, optimized from %s to %s tiles, %s palettes used. Wasted %s seconds' % (stats.totalTiles, stats.actualTiles, stats.actualPalettes, stats.timeWasted))

def debugLogTileStatus(tiles):
  for tile in tiles:
    debugLog({
      'id'  : tile['id'],
      'refId'  : tile['refId'],
      'xMirror'  : tile['xMirror'],
      'yMirror'  : tile['yMirror'],
    }, 'tile %s' % tile['id'])
  

def getReferencePaletteImage( options ):
	return getInputImage(options, options.get('refpalette')) if options.get('refpalette') else []

  
def writeOutputFiles(tiles, palettes, image, options):
  outTiles = augmentOutIds(tiles)
  outPalettes = augmentOutIds(palettes)
  
  #writeTiles( outTiles, options )
  tileFile = getOutputFile( options, ext='tiles' )
  [tileFile.write(char) for char in getTileWriteStream( outTiles, options )] 
  tileFile.close

  if not options.get('directcolor'):
    #writePalettes( outPalettes, options )
    palFile = getOutputFile( options, ext='palette' )
    [palFile.write(char) for char in getPaletteWriteStream( outPalettes, options )] 
    palFile.close
    if options.get('verify'):
      writeSamplePalette(outPalettes, options)

  #writeTileMap( outTiles, outPalettes, options )
  tilemapFile = getOutputFile( options, ext='tilemap' )
  tilemapStream = getSpriteTileMapStream(tiles, palettes, options) if options.get('mode') == 'sprite' else getBgTileMapStream(tiles, palettes, options)
  [tilemapFile.write(char) for char in tilemapStream] 
  tilemapFile.close
  
  if options.get('verify'):
	writeSampleImage(outTiles, outPalettes, image, options)


def augmentOutIds(elements):
  outElements = []
  outId = 0
  for element in elements:
	if element['refId'] == None:
	  element['outId'] = outId
	  outId += 1
	else:
	  element['outId'] = None
	outElements.append(element)
	
  return outElements

def writeSamplePalette(palettes, options):
  '''ugly hack, used to provide output sample w/o having to load the created files in an SNES program'''
  realPalettes = [pal for pal in palettes if pal['refId'] == None]
  sample = Image.new( "RGB", ( 2 ** options.get('bpp'), len(realPalettes) ), convertColorSnesToRGB(options.get('transcol')))
  for yPos in range(len(realPalettes)):
	for xPos in range( 2 ** options.get('bpp') ):
	  try:
		color = realPalettes[yPos]['color'][xPos]
	  except IndexError:
		color = EMPTY_COLOR
	  sample.putpixel((xPos,yPos),convertColorSnesToRGB(color))
  outFileName = "%s.%s" % ( options.get('outfilebase'), 'sample_palette.png' )
  sample.save( outFileName, 'PNG' )


def writeSampleImage(tiles, palettes, image, options):
  '''ugly hack, used to provide output sample w/o having to load the created files in an SNES program'''
  sample = Image.new( "RGB", ( image['resolutionX'], image['resolutionY'] ), convertColorSnesToRGB( options.get('transcol') ) )
  for tile in tiles:
    tileConfig = fetchTileConfig( tile, tiles, palettes )
    if not options.get('directcolor'):
      tile['pixel'] = tiles[tileConfig['tileId']]['indexedPixel']	#hack, copy pixels of referenced tile into current tile

    actualTile = mirrorTile( tile, { 'x' : tileConfig['xMirror'], 'y' : tileConfig['yMirror'] } )
    actualPalette = palettes[tileConfig['palId']]
    for yPos in range(len(actualTile['pixel'])):
      for xPos in range(len(actualTile['pixel'][yPos])):
        if options.get('directcolor'):
          #source: -bbbbbgg gggrrrrr target: -bb---gg g--rrr--
          pixel = actualTile['pixel'][yPos][xPos] &  0x639c
        else:
          colorIndex = actualTile['pixel'][yPos][xPos]
          try:
            pixel = actualPalette['color'][colorIndex]
          except IndexError:
            debugLog(actualPalette, 'bad palette index %s requested' % colorIndex)
            pixel = EMPTY_COLOR
        pixelColor = convertColorSnesToRGB(pixel)
        pixelPos = (actualTile['x']+xPos, actualTile['y']+yPos)
        try:
          sample.putpixel(pixelPos,pixelColor)
        except IndexError:
          debugLog(pixelPos, 'bad pixel position')
  outFileName = "%s.%s" % ( options.get('outfilebase'), 'sample.png' )
  #logging.debug("wrote sample image '%s'." % outFileName)
  sample.save( outFileName, 'PNG' )


def parseTiles(image, options):
  return parseSpriteTiles(image, options) if options.get('mode') == 'sprite' else parseBgTiles(image, options)


def writeTileMap(tiles, palettes, options):
  if options.get('mode') == 'sprite':
	writeSpriteTileMap(tiles, palettes, options)
  else:
	writeBgTileMap(tiles, palettes, options)



def getBgTileMapStream(tiles, palettes, options):
  '''writes successive blocks of 32x32 tile tilemaps'''
  stream = []
  bgTilemaps = getBgTilemaps(tiles, palettes, options)
  for tile in [tile for tilemap in bgTilemaps for tile in tilemap]:
	stream.append( chr( tile & 0xff ) )
	stream.append( chr( (tile & 0xff00) >> 8 ) )
  return stream


def writeBgTileMap(tiles, palettes, options):
  '''writes successive blocks of 32x32 tile tilemaps'''
  bgTilemaps = getBgTilemaps(tiles, palettes, options)
  outFile = getOutputFile( options, ext='tilemap' )
  for tile in [tile for tilemap in bgTilemaps for tile in tilemap]:
	outFile.write( chr( tile & 0xff ) )
	outFile.write( chr( (tile & 0xff00) >> 8 ) )
  outFile.close()


def getBgTilemaps(tiles, palettes, options):
  emptyTile = getEmptyTileConfig(tiles, palettes)
  bgTilemaps = [[emptyTile['concatConfig'] for i in range(BG_TILEMAP_SIZE * BG_TILEMAP_SIZE)] for i in range(getCurrentTilemap(options.get('resolutionx'), options.get('resolutiony'), options) + 1)]
  for tile in tiles:
    mapId = getCurrentTilemap(tile['x'], tile['y'], options)
    tilePos = getPositionInTilemap(tile['x'], tile['y'], options)
    tileConfig = fetchTileConfig( tile, tiles, palettes )['concatConfig']

    try:
      bgTilemaps[mapId][tilePos] = tileConfig
    except IndexError:
      logging.error( 'invalid tilemap access in getBgTilemaps, mapId: %s, tilePos: %s' % (mapId, tilePos) )
  return bgTilemaps


def getEmptyTileConfig(tiles, palettes):
  '''scans for empty tile, returns fake value if none found '''
  '''todo, do we really need an additional empty tile here sometimes?'''
  emptyTiles = [tile for tile in tiles if tileIsEmpty(tile)]
  try:
	return fetchTileConfig( emptyTiles.pop(), tiles, palettes )
  except IndexError:
	return { 'concatConfig': 0 }
	
	
def tileIsEmpty(tile):
  if tile['refId'] != None:
	return False
  for pixel in [pixel for scanline in tile['indexedPixel'] for pixel in scanline]:
	if pixel != 0:
	  return False
  return True


def getPositionInTilemap(xPos, yPos, options):
  xTilePos = int(math.floor((xPos / options.get('tilesizex')) % BG_TILEMAP_SIZE))
  yTilePos = int(math.floor((yPos / options.get('tilesizey')) % BG_TILEMAP_SIZE))
  return (BG_TILEMAP_SIZE * yTilePos) + xTilePos


def getCurrentTilemap(xPos, yPos, options):
  return int(math.floor(xPos / float(BG_TILEMAP_SIZE * options.get('tilesizex'))) * math.floor(yPos / float(BG_TILEMAP_SIZE * options.get('tilesizey'))))


def getSpriteTileMapStream( tiles, palettes, options ):
  stream = []
  for tile in tiles:
	tileConfig = fetchSpriteTileConfig( tile, tiles, palettes )
	stream.append( chr( tileConfig['x'] & 0xff ) )
	stream.append( chr( tileConfig['y'] & 0xff ) )
	stream.append( chr( tileConfig['concatConfig'] & 0xff ) )
	stream.append( chr( (tileConfig['concatConfig'] & 0xff00) >> 8 ) )
  return stream

def writeSpriteTileMap( tiles, palettes, options ):
  outFile = getOutputFile( options, ext='spritemap' )
  for tile in tiles:
	tileConfig = fetchSpriteTileConfig( tile, tiles, palettes )
	outFile.write( chr( tileConfig['concatConfig'] & 0xff ) )
	outFile.write( chr( (tileConfig['concatConfig'] & 0xff00) >> 8 ) )
	outFile.write( chr( tileConfig['x'] & 0xff ) )
	outFile.write( chr( tileConfig['y'] & 0xff ) )
  outFile.close()


def fetchTileConfig( tile, tiles, palettes ):
  actualTile = fetchActualTile( tiles, tile['id'], False, False )
  actualPalette = fetchActualEntity( palettes, actualTile['palette']['id'] )
  x = 1 if actualTile['xMirror'] else 0
  y = 1 if actualTile['yMirror'] else 0
  return {
	'x' : tile['x'],
	'y' : tile['y'],
	'xMirror' : actualTile['xMirror'],
	'yMirror' : actualTile['yMirror'],
	'tileId' : actualTile['id'],
	'palId' : actualPalette['id'],
	'tileOutId' : actualTile['outId'],
	'palOutId' : actualPalette['outId'],	
	'concatConfig' : (y << 15) | (x << 14) | ((actualPalette['outId'] & 0x7) << 10) | (actualTile['outId'] & 0x3ff)
  }


def fetchSpriteTileConfig( tile, tiles, palettes ):
  actualTile = fetchActualTile( tiles, tile['id'], False, False )
  actualPalette = fetchActualEntity( palettes, actualTile['palette']['id'] )
  priority = 0x3
  nametable = 0x0
  x = 1 if tile['xMirror'] else 0
  y = 1 if tile['yMirror'] else 0
  return {
	'x' : tile['x'],
	'y' : tile['y'],
	'xMirror' : tile['xMirror'],
	'yMirror' : tile['yMirror'],
	'tileId' : actualTile['id'],
	'palId' : actualPalette['id'],
	'tileOutId' : actualTile['outId'],
	'palOutId' : actualPalette['outId'],	
	'concatConfig' : (y << 15) | (x << 14) | (priority << 12) | ((actualPalette['outId'] & 0x7) << 9) | (nametable << 8) | (actualTile['outId'] & 0x3ff)
  }

'''
format sprite tilemap (spritetilemap):
  x/y-offset relative to upper left corner of source image
  byte	0			1			2		3
		  cccccccc	vhopppcc	x-off	y-off
target format sprite tilemap:
  byte	0			1			2		3
		  x-off   y-off cccccccc	vhoopppN
'''

def writeTiles( tiles, options ):
  outFile = getOutputFile( options, ext='tiles' )
  for tile in tiles:
	if tile['refId'] == None:
	  writeBitplaneTile( outFile, tile, options )
  outFile.close()


def writeBitplaneTile( outFile, tile, options ):
  bitplanes = fetchBitplanes( tile, options )
  for i in range( 0, len( bitplanes ), 2 ):
	while bitplanes[i].notEmpty():
	  outFile.write( chr( bitplanes[i].first() ) )
	  outFile.write( chr( bitplanes[i+1].first() ) )


def getTileWriteStream( tiles, options ):
  stream = []
  for tile in tiles:
	if tile['refId'] == None:
	  bitplanes = fetchBitplanes( tile, options )
	  for i in range( 0, len( bitplanes ), 2 ):
		while bitplanes[i].notEmpty():
		  stream.append(( chr( bitplanes[i].first() ) ))
		  stream.append(( chr( bitplanes[i+1].first() ) ))
  return stream

def getPaletteWriteStream( palettes, options ):
  stream = []
  for color in [pixel for palette in [palette for palette in palettes if palette['refId'] == None] for pixel in palette['color']]:
	stream.append(chr((color & 0xff)))
	stream.append(chr((color & 0xff00) >> 8 ))
  return stream

def fetchBitplanes( tile, options ):
  bitplanes = []
  for bitPlane in range( options.get('bpp') ):
    bitplaneTile = BitStream()
    #debugLog(tile['pixel'],'native')
    #debugLogExit(tile['indexedPixel'],'indexed')
    target = 'pixel' if options.get('directcolor') else 'indexedPixel' 
    for pixel in [pixel for scanline in tile[target] for pixel in scanline]:
      if options.get('directcolor'):
        #source: -bbbbbgg gggrrrrr target: BBGGGRRR
        #pixel = ((pixel & 0x7c00) >> 10) | ((pixel & 0x380) >> 7) | ((pixel & 0x1c) >> 2)
        pixel = (((pixel & 0x6000) >> 7) | ((pixel & 0x380) >> 4) | ((pixel & 0x1c) >> 2))
      bitplaneTile.writeBit( pixel >> bitPlane )
    bitplanes.append( bitplaneTile )
  return bitplanes


def writePalettes( palettes, options ):
  outFile = getOutputFile( options, ext='palette' )
  for color in [pixel for palette in [palette for palette in palettes if palette['refId'] == None] for pixel in palette['color']]:
	outFile.write(chr((color & 0xff)))
	outFile.write(chr((color & 0xff00) >> 8 ))
  outFile.close()


def getOutputFile( options, ext ):
  outFileName = "%s.%s" % ( options.get('outfilebase'), ext )
  try:
	outFile = open( outFileName, 'wb' )
  except IOError:
	logging.error( 'unable to access output file %s' % outFileName )
	sys.exit(1)
  return outFile


def palettizeTiles( tiles, palettes ):
  '''replaces direct tile colors with best-matching entries of assigned palette'''
  return [(tile if tile['refId'] != None else palettizeTile( tile, palettes )) for tile in tiles]


def findOptimumTilePalette(palettes, pixels):
  optimumPalette = { 'error' : INFINITY }
  for palette in [pal for pal in palettes if pal['refId'] == None]:
	squareError = 0
	for similarColor in [getSimilarColor( pixel, palette['color'] ) for scanline in pixels for pixel in scanline]:
		squareError += similarColor['error'] * similarColor['error']
	palette['error'] = math.sqrt(squareError)
	optimumPalette = palette if palette['error'] < optimumPalette['error'] else optimumPalette
  return optimumPalette


def palettizeTile( tile, palettes ):
  #logging.debug('palettizing tile %s' % tile['id'])
  palette = findOptimumTilePalette(palettes, tile['pixel'])

  indexedScanlines = []
  scanlines = []
  
  for scanline in tile['pixel']:
	indexedPixels = []
	pixels = []
	for pixel in scanline:
	  similarColor = getSimilarColor( pixel, palette['color'] )
	  indexedPixels.append( palette['color'].index(similarColor['value']) )
	  pixels.append(similarColor['value'])
	#indexedPixels.append( [getSimilarColorIndex( pixel, palette['color'] ) for pixel in scanline] )
	scanlines.append(pixels)
	indexedScanlines.append(indexedPixels)
  return {
	'indexedPixel'	: indexedScanlines,
	'pixel'			: scanlines,
	'palette'			: {
	  'color'				: [],
	  'id'				: palette['id'],
	  'refId'				: None
	},
	'id'			: tile['id'],
	'refId'			: tile['refId'],
	'x'				: tile['x'],
	'y'				: tile['y'],
	'xMirror'		: tile['xMirror'],
	'yMirror'		: tile['yMirror']
  }


def fetchActualTile( entities, entityId, xStatus, yStatus ):
  if entities[entityId]['refId'] == None:
    #logging.debug('actual    %s[%s%s]' % (entityId, 'X' if entities[entityId]['xMirror'] else 'x', 'Y' if entities[entityId]['yMirror'] else 'y'))
    tile = entities[entityId]
    tile['xMirror'] = xStatus
    tile['yMirror'] = yStatus
    return tile
    '''
    return {
      'indexedPixel'  : entities[entityId]['indexedScanlines'],
      'pixel'         : entities[entityId]['scanlines'],
      'palette'       : entities[entityId]['palette'],
      'id'            : entities[entityId]['id'],
      'refId'         : entities[entityId]['refId'],
      'x'             : entities[entityId]['x'],
      'y'             : entities[entityId]['y'],
      'xMirror'       : xStatus,
      'yMirror'       : yStatus
    }
    '''
    #tile = entities[entityId]

  else:
    #logging.debug('reference %s[%s%s]->%s[%s%s]' % (entityId, 'X' if entities[entityId]['xMirror'] else 'x', 'Y' if entities[entityId]['yMirror'] else 'y', entities[entityId]['refId'], 'X' if entities[entities[entityId]['refId']]['xMirror'] else 'x', 'Y' if entities[entities[entityId]['refId']]['yMirror'] else 'y'))
    return fetchActualTile( entities, entities[entityId]['refId'], entities[entityId]['xMirror'] ^ xStatus, entities[entityId]['yMirror'] ^ yStatus )

    #beide gesetzt:0
    #1 gesetzt: 1
    #keins gesetzt: 0
    '''
    debugLog({
      'id'  : tile['id'],
      'refId'  : tile['refId'],
      'xMirror'  : tile['xMirror'],
      'yMirror'  : tile['yMirror'],
    }, 'tile %s[%s%s]->%s[%s%s]' % tile['id'])
    '''
    #tile['yMirror'] = tile['yMirror'] ^ entities[entityId]['yMirror']
    #tile['xMirror'] = tile['xMirror'] ^ entities[entityId]['xMirror']

  #logging.debug('returning %s[%s%s]' % (tile['id'], 'X' if tile['xMirror'] else 'x', 'Y' if tile['yMirror'] else 'y'))
  #return tile


def fetchActualEntity( entities, entityId ):
  return entities[entityId] if entities[entityId]['refId'] == None else fetchActualEntity( entities, entities[entityId]['refId'] )

def parsePalettes( tiles, options ):
  return [reducePaletteColorDepth( tile['palette'], options ) for tile in tiles]


def parseGlobalPalettes( tiles, options ):
  globalPalette = fetchGlobalPalette(tiles, options)
  while(len(globalPalette) > (((options.get('bpp') ** 2) - 1) * options.get('palettes'))):
	nearestIndices = getNearestPaletteIndices( globalPalette )
	globalPalette.pop( max( nearestIndices['id1'], nearestIndices['id2'] ) )
	#logging.debug('global palette length now at %s, target is %s.' % (len(globalPalette), (((options.get('bpp') ** 2) - 1) * options.get('palettes'))))
  return partitionGlobalPalette(globalPalette, options)


def partitionGlobalPalette(palettes, options):
  partitionedPalettes = []
  paletteCount = int(math.ceil(len(palettes)/float(((options.get('bpp') ** 2) - 1))))
  for palIndex in range(paletteCount):
	palette = []
	palette.append(options.get('transcol'))
	for colorIndex in range((options.get('bpp') ** 2) - 1):
	  try:
		palette.append(palettes.pop(0))
	  except IndexError:
		palette.append(EMPTY_COLOR)
	  
	partitionedPalettes.append({
	  'color' : palette,
	  'refId'	: None,
	  'id'	: palIndex
	})
  return partitionedPalettes


def fetchGlobalPalette(tiles, options):
  refPaletteImg = getReferencePaletteImage(options)
  if refPaletteImg:
	return [color for color in set([pixel for scanline in refPaletteImg['pixels'] for pixel in scanline if pixel != options.get('transcol')])]
  else:
	return sorted([color for color in set([color for tile in tiles for color in tile['palette']['color'] if color != options.get('transcol')])],sortSNESColors)


def checkPaletteCount( palettes, options):
  palCount = len( [pal for pal in palettes if pal['refId'] == None] )
  if ( palCount > options.get('palettes') ):
	logging.error( 'Image needs %s palettes, exceeds allowed amount of %s.' % ( palCount, options.get('palettes') ) )
	sys.exit(1)
    

def optimizePalettes( palettes, options ):
  return [getNearestPalette( palette, palettes, options ) for palette in palettes]
  

def getPaletteById(palettes, palId):
  for palette in [pal for pal in palettes if pal['id'] == palId]:
	return palette
  logging.error( 'Unable find palette id %s in getPaletteById.' % palId )
  sys.exit(1)
  

def getSimilarPalette( inputPalette, refPalette ):
  squareError = 0
  for color in inputPalette['color']:
	similarColor = getSimilarColor( color, refPalette['color'] )
	squareError += similarColor['error'] * similarColor['error']
  return {
	'color' : [],#colors,
	'refId'	: refPalette['id'],
	'id'	: inputPalette['id'],
	'error'	: math.sqrt( squareError )
  }


def getSimilarColor( color, refPalette ):
  minError = {
	'error'	: INFINITY,
	'value'	: None
  }
  for refColor in refPalette:
	diff = compareSNESColors( color, refColor )
	minError = minError if minError['error'] < diff else {
	  'error'	: diff,
	  'value'	: refColor
	}
  return minError


def getSimilarColorIndex( color, refPalette ):
  similarColor = getSimilarColor( color, refPalette )
  return refPalette.index( similarColor['value'] )
  
  
def reducePaletteColorDepth( palette, options ):
  while len( palette['color'] ) > ( options.get('bpp') * options.get('bpp') ):
	nearestIndices = getNearestPaletteIndices( palette['color'] )
	palette['color'].pop( max( nearestIndices['id1'], nearestIndices['id2'] ) )
  return palette

  
def getNearestPaletteIndices( palette ):
  diffTable = {}
  for i in range( 1, len( palette ) ):
	for iRef in range( 1, len( palette ) ):
	  if i != iRef:
		diffIndex = "%s-%s" % ( min( i, iRef ), max( i, iRef ) )
		diffTable[diffIndex] = {
		  'difference'	: compareSNESColors( palette[i], palette[iRef] ),
		  'id1'			: i,
		  'id2'			: iRef
		}
  return getMinDifferenceIds( diffTable )


def getMinDifferenceIds( diffTable ):
  minDiff = { 'difference' : INFINITY }
  for diffName, diff in diffTable.iteritems():
	minDiff = diff if diff['difference'] < minDiff['difference'] else minDiff
  return minDiff


def optimizeTiles( tiles, options ):
  return [checkDuplicateTileFast( tile, tiles, options ) for tile in tiles]

def checkDuplicateTile( tile, refTiles, options ):
  #logging.debug('optimizing tile %s of %s' % (tile['id'],len(refTiles)))
  optimumTile = { 'error' : INFINITY, 'id' : None }
  for refTile in refTiles[:tile['id']]:
	for replacedTile in [compareTile( mirrorTile, refTile ) for mirrorTile in mirrorTiles( tile )]:
	  optimumTile = optimumTile if replacedTile['error'] > optimumTile['error'] else replacedTile
  return optimumTile if optimumTile['error'] < float(options.get('tilethreshold')) and optimumTile['id'] else tile


def checkDuplicateTileFast( tile, refTiles, options ):
  '''ugly but fast(er)'''
  #logging.debug('optimizing tile %s of %s' % (tile['id'],len(refTiles)))
  optimumTile = { 'error' : INFINITY, 'id' : None }
  mirroredTiles = mirrorTiles( tile )
  
  #cmpStart = tile['id'] - min(LOOKBACK_TILES, tile['id'])
  #look back through all tiles!
  cmpStart = 0
  for refTile in refTiles[cmpStart:tile['id']]:
	refPixels = [pixel for scanline in refTile['pixel'] for pixel in scanline]
	for mirrorTile in mirroredTiles:
	  squareError = 0
	  inPixels = [pixel for scanline in mirrorTile['pixel'] for pixel in scanline]

	  for i in range(len(inPixels)):
		r = (inPixels[i] & 0x1f) - (refPixels[i] & 0x1f)
		g = ((inPixels[i] & 0x3E0)>>5) - ((refPixels[i] & 0x3E0)>>5)
		b = ((inPixels[i] & 0x7C00)>>10) - ((refPixels[i] & 0x7C00)>>10)
		redMean = (inPixels[i] & 0x1f) + (refPixels[i] & 0x1f) / 2
		squareError += math.sqrt((((512+redMean)*r*r)>>8) + 4*g*g + (((767-redMean)*b*b)>>8))**2
	  error = math.sqrt( squareError )
	  if error <= optimumTile['error']:
		optimumTile = {
		  'id'		: mirrorTile['id'],
		  'pixel': [],
		  'indexedPixel': [],
		  'palette' : {
			'color'		: [],
			'id'		: mirrorTile['palette']['id'],
			'refId'		: refTile['palette']['id']
		  },
		  'x'			: mirrorTile['x'],
		  'y'			: mirrorTile['y'],
		  'refId'		: refTile['id'],
		  'error'		: error,
		  'xMirror'	: mirrorTile['xMirror'],
		  'yMirror'	: mirrorTile['yMirror']
		}
  return optimumTile if optimumTile['error'] < options.get('tilethreshold') and optimumTile['id'] else tile


def compareTile( inputTile, refTile ):
  squareError = 0
  inPixels = [pixel for scanline in inputTile['pixel'] for pixel in scanline]
  refPixels = [pixel for scanline in refTile['pixel'] for pixel in scanline]
  for error in [compareSNESColors( inPixels[i], refPixels[i]) for i in range(len(inPixels))]:
	squareError += error * error
  return {
	'id'		: inputTile['id'],
	'pixel': [],
	'palette' : {
	  'color'		: [],
	  'id'		: inputTile['palette']['id'],
	  'refId'		: refTile['palette']['id']
	},
	'x'			: inputTile['x'],
	'y'			: inputTile['y'],
	'refId'		: refTile['id'],
	'error'		: math.sqrt( squareError ),
	'xMirror'	: inputTile['xMirror'],
	'yMirror'	: inputTile['yMirror']
  }

  
def mirrorTiles( tile):
  return [
	tile,
	mirrorTile( tile, { 'x' : True, 'y' : False } ),
	mirrorTile( tile, { 'x' : False, 'y' : True } ),
	mirrorTile( tile, { 'x' : True, 'y' : True } ),
  ]


def mirrorTile( tile, config ):
  mirrorTile = []
  verticalRange = range( len( tile['pixel'] )-1, 0-1, -1 ) if config['y'] else range( len( tile['pixel'] ) )
  for yPos in verticalRange:
	horizontalRange = range( len( tile['pixel'][yPos] )-1, 0-1, -1 ) if config['x'] else range( len( tile['pixel'][yPos] ) )
	mirrorTile.append( [tile['pixel'][yPos][xPos] for xPos in horizontalRange] )
  return {
	'id'		: tile['id'],
	'pixel'		: mirrorTile,
	'palette'		: tile['palette'],
	'x'			: tile['x'],
	'y'			: tile['y'],
	'refId'		: None,
	'xMirror'	: config['x'],
	'yMirror'	: config['y']
  }


def sortSNESColors( SNESCol1, SNESCol2 ):
  color1 = ColObj(SNESCol1)
  color2 = ColObj(SNESCol2)
  return -1 if color1.getHue() - color2.getHue() < 0 else 1
   

def compareSNESColors( SNESCol1, SNESCol2 ):
  color1 = ColObj(SNESCol1)
  color2 = ColObj(SNESCol2)
  redMean = color1.r + color2.r / 2
  r = color1.r - color2.r
  g = color1.g - color2.g
  b = color1.b - color2.b
  return math.sqrt((((512+redMean)*r*r)>>8) + 4*g*g + (((767-redMean)*b*b)>>8))


def compareSNESColor( col1, col2 ):
  return max( col1, col2 ) - min( col1, col2 )


def parseSpriteTiles( image, options ):
  pos = getInitialSpritePosition( image, options )
  tiles = []
  while pos['y'] < image['resolutionY']:
    pos['x'] = 0
    while pos['x'] < image['resolutionX']:
      if checkVlineFilled( image, pos, options ):
	tile = fetchTile( image, pos, options, len( tiles ) )
	tiles.append( {
	  'id'		: len( tiles ),
	  'pixel'	: tile['pixel'],
	  'palette'	: tile['palette'],
	  'x'		: pos['x'],
	  'y'		: pos['y'],
	  'refId'	: None,
	  'xMirror'	: False,
	  'yMirror'	: False
	} )
	pos['x'] += options.get('tilesizex')
      else:
	pos['x'] += 1
    pos['y'] += options.get('tilesizey')
  logging.info("parsed %s oam sprite tiles" % len(tiles))
  return tiles


def checkVlineFilled( image, pos, options ):
  for ypos in range( pos['y'], pos['y']+options.get('tilesizey') ):
    if isPixelOpaque( image['pixels'], ypos, pos['x'], options ):
      return True
  return False


def isPixelOpaque( pixels, yPos, xPos, options ):
  return getPixel( pixels, yPos, xPos, options ) != options.get('transcol')


def getPixel( pixels, yPos, xPos, options ):
  try:
	return pixels[yPos][xPos]
  except IndexError:
	 return options.get('transcol')


def getInitialSpritePosition( image, options ):
  for scanline in range( len( image['pixels'] ) ):
	for pixel in range( len( image['pixels'][scanline] ) ):
	  if isPixelOpaque( image['pixels'], scanline, pixel, options ):
		return {
		  'y' : scanline,
		  'x' : getInitialLeftmostPixelSprite( image, scanline, options )
		}
  return {	#no match found, be stupid and loop anyway
	'y' : 0,
	'x' : 0
  }


def getInitialLeftmostPixelSprite( image, top, options ):
  x = INFINITY
  for scanline in range( top, top + options.get('tilesizey') ):
    for pixel in range( len( image['pixels'][scanline] ) ):
	  if isPixelOpaque( image['pixels'], scanline, pixel, options ):
		x = min( x, pixel )
  return x


def parseBgTiles( image, options ):
  '''normal bg tiles, parse whole image in tilesize-steps'''
  pos = {
    'x' : 0,
    'y' : 0
  }
  tiles = []
  while pos['y'] < image['resolutionY']:
	pos['x'] = 0
	while pos['x'] < image['resolutionX']:
	  tile = fetchTile( image, pos, options, len( tiles ) )
	  tiles.append( {
		'id' 		: len( tiles ),
		'pixel'		: tile['pixel'],
		'palette'	: tile['palette'],
		'x'			: pos['x'],
		'y'			: pos['y'],
		'refId'		: None,
		'xMirror'	: False,
		'yMirror'	: False
	  } )
	  pos['x'] += options.get('tilesizex')
	pos['y'] += options.get('tilesizey')
  return tiles


def fetchTile( image, pos, options, tileId ):
  tile = []
  palette = [options.get('transcol')]
  #logging.debug('fetching tile %s' % tileId)
  for yPos in range( pos['y'], pos['y']+options.get('tilesizey') ):
    tileLine = []
    for xPos in range( pos['x'], pos['x']+options.get('tilesizex') ):
	  pixel = getPixel( image['pixels'], yPos, xPos, options )
	  tileLine.append( pixel )
	  if pixel not in palette:
		palette.append( pixel )
    tile.append( tileLine )    
  return {
	'pixel'		: tile,
	'palette'	: {
	  'id'			: tileId,
	  'color'		: palette,
	  'refId'	: None
	}
  }


def getInputImage( options, filename ):
  #logging.debug('parsing input image.')
  try:
	  inputImage = Image.open( filename )
  except IOError:
	  logging.error( 'Unable to load input image "%s"' % filename )
	  sys.exit(1)
  
  paddedImage = padImageReduceColdepth( inputImage, options )
  options.set('resolutionx', paddedImage.size[0])
  options.set('resolutiony', paddedImage.size[1])

  return {
	'resolutionX'	: paddedImage.size[0],
	'resolutionY'	: paddedImage.size[1],
	'pixels'	: getSnesPixels( paddedImage )
  }


def getSnesPixels( image ):
  '''extract color-converted pixels from image'''
  rawPixels = list(image.getdata())
  outputPixels = []
  for y in range( image.size[1] ):
	outputPixels.append( [] )
	for x in range( image.size[0] ):
	  outputPixels[y].append( convertColorRGBToSnes( rawPixels.pop(0) ) )
  return outputPixels
  
  
def padImageReduceColdepth( inputImage, options):
  '''pad image to multiple of tilesize, fill blank areas with transparent color'''
  paddedWidth = inputImage.size[0] if ( inputImage.size[0] % options.get('tilesizex') == 0 ) else ( inputImage.size[0] - ( inputImage.size[0] % options.get('tilesizex') ) + options.get('tilesizex') )
  paddedHeight = inputImage.size[1] if ( inputImage.size[1] % options.get('tilesizey') == 0 ) else ( inputImage.size[1] - ( inputImage.size[1] % options.get('tilesizey') ) + options.get('tilesizey') )
    
  paddedImage = Image.new( 'RGB', ( paddedWidth, paddedHeight ), convertColorSnesToRGB( options.get('transcol') ) )
  paddedImage.paste( inputImage, ( 0, 0 ) )
  
  colorCount = (((options.get('bpp') ** 2) - 1) * options.get('palettes'))
  #logging.info('Reducing to %s colors.' % colorCount)
  reducedImage = paddedImage.convert('P', palette=Image.ADAPTIVE, colors=colorCount).convert('RGB')
  #logging.debug('Done reducing colors.')
  return reducedImage


def convertColorSnesToRGB( inputColor ):
  '''returns 16bit color list, format: (r,g,b)'''
  r = ( inputColor & 0x1f ) << 3
  g = ( inputColor & 0x3E0 ) >> 2
  b = ( inputColor & 0x7c00 ) >> 7
  return (
	r | (r >> 5),
	g | (g >> 5),
	b | (b >> 5)
  )


def convertColorRGBToSnes( inputColor ):
  '''returns 5bit color tuple, format: -bbbbbgg gggrrrrr'''
  return ( (inputColor[0] & 0xf8) >> 3 ) | ( (inputColor[1] & 0xf8) << 2 ) | ( (inputColor[2] & 0xf8) << 7 )

  #  options['outfilebase']['value'] = args.pop()	#last argument should be output filename
  #  options['infile']['value'] = args.pop()	#before-last argument should be input filename

class BitStream():
  def __init__( self ):
	self.bitPos = 7
	self.byte = 0
	self.bitStream = []
	
  def writeBit(self, bit):
	self.byte |= (bit & 1) << self.bitPos
	self.bitPos -= 1
	if self.bitPos < 0:
	  self.bitStream.append(self.byte)
	  self.byte = 0
	  self.bitPos = 7

  def get(self):
	return self.bitStream

  def first(self):
	return self.bitStream.pop(0)

  def notEmpty(self):
	return len(self.bitStream) > 0


class Statistics():
  def __init__(self, tiles, palettes, startTime):
	self.totalTiles = len(tiles)
	self.actualTiles = len([tile for tile in tiles if tile['refId'] == None])
	self.actualPalettes = len([pal for pal in palettes if pal['refId'] == None])
	self.timeWasted = time.clock() - startTime


class ColObj():
  def __init__(self, snesCol):
	self.r = snesCol & 0x1f
	self.g = (snesCol & 0x3E0)>>5
	self.b = (snesCol & 0x7C00)>>10

  def getLightness(self):
	r = self.r / float(0x1f)
	g = self.g / float(0x1f)
	b = self.b / float(0x1f)
	
	cmin = min(r, g, b)
	cmax = max(r, g, b)
	return (cmax + cmin) / 2

  def getSaturation(self):
	r = self.r / float(0x1f)
	g = self.g / float(0x1f)
	b = self.b / float(0x1f)
	
	cmin = min(r, g, b)
	cmax = max(r, g, b)
	cdelta = cmax - cmin
	if cdelta == 0:
	  return 0
	clight = (cmax + cmin) / 2
	return cdelta / (cmax + cmin) if clight < 0.5 else cdelta / (2 - cmax - cmin)

  def getHue(self):
	r = self.r / float(0x1f)
	g = self.g / float(0x1f)
	b = self.b / float(0x1f)
	
	cmin = min(r, g, b)
	cmax = max(r, g, b)
	cdelta = cmax - cmin
	if cdelta == 0:
	  return 0
	clight = (cmax + cmin) / 2
	csaturation = cdelta / (cmax + cmin) if clight < 0.5 else cdelta / (2 - cmax - cmin)
	
	rdelta =(((cmax-r)/6)+(cdelta/2)) / cdelta
	gdelta =(((cmax-g)/6)+(cdelta/2)) / cdelta
	bdelta =(((cmax-b)/6)+(cdelta/2)) / cdelta
	
	if r == cmax:
	  chue = bdelta - gdelta
	elif g == cmax:
	  chue = (1/3) + rdelta - bdelta
	elif b == cmax:
	  chue = (2/3) + gdelta - rdelta

	if chue < 0:
	  chue += 1
	if chue > 1:
	  chue -= 1
	return chue


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

