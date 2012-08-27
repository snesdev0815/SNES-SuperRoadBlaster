.include "src/config/config.inc"

/*
.ramsection "oop obj ram zp" bank 0 slot 2

.ends
*/


.define MSU1_SEEK_TIMEOUT $2000
.define MSU1_MAX_TILE_TRANSFER_LENGTH $2000
.define MSU1_CHUNK_DIFFERENCE $380
.define MSU1_NEXT_VIDEO_SCHEDULED $80
.define MSU1_FRAME_CYCLE_COUNT $ff
.define MSU1_VIDEOMODE_THRESHOLD $0400
.define MSU1_NEXT_VIDEO_DELAY 1 ;make sure msu1 dma transfers are flushed before seeking to new video. increasing this above 1 creates frame number to go apeshit, wtf???

;quick hack, this should be defined in video handler, not msu interface
.define VRAM_TILEMAP	0
.define VRAM_TILEMAP.LENGTH	$800
.define VRAM_TILES	$2000
.define CGRAM_PALETTE	0
;.define V_SCROLL	-33
.define V_SCROLL    0




.struct MSU1_FILE
  ID	ds 6
  TITLE ds 21
  BPP db
  FPS db
  CHAPTERCOUNT db
  CHECKSUM ds 2
  POINTER ds 4
.endst

.struct MSU1_CHAPTER
  ID	db
  FRAMECOUNT ds 3
  POINTER ds 4
.endst

.struct MSU1_FRAME
  ID dw
  TILEMAPSIZE	dw
  TILESIZE dw
  FRAMEDATA ds 0
.endst

.define MSU1_FILE.TITLE.LEN 21

.define MSU1.FRAMEBUFFER.COUNT 2
.define MSU1.FRAMEBUFFER.TILESIZE MSU1_MAX_TILE_TRANSFER_LENGTH * 2
.define MSU1.FRAMEBUFFER.PALETTESIZE $80 * 2

.struct msu1Struct
  tmp ds 8
  bpp	db
  fps db
  frameCount dw
  chapterCount dw
  currentFrame dw
  currentFramePointer ds 4
  currentChapter db
  currentChapterPointer ds 4
  currentTrack db
  nextChapter db
  videoPlaying db
  paletteLength dw
  tilemapLength dw
  tilesLength dw
  framebuffer.1.obj ds 4
  framebuffer.1.tiles dw
  framebuffer.1.tilemap dw
  framebuffer.1.palette dw
  framebuffer.2.obj ds 4
  framebuffer.2.tiles dw
  framebuffer.2.tilemap dw
  framebuffer.2.palette dw
  framebuffer.current.tiles dw
  framebuffer.current.tilemap dw
  framebuffer.current.palette dw
  framebuffer.current.pointer dw
  currentFramebuffer ds 4
  currentStart dw
  currentLength dw
  frameCycle db
  frameBusy db
  frameWait db
  tileTransferRemainder dw
  tileTransferOffset dw
  videoMask ds 4
  videoMode db
.endst

;zp-vars
.enum 0
  iterator INSTANCEOF iteratorStruct
  this INSTANCEOF msu1Struct
/*
_tmp ds 8
msu1Bpp ds 1
msu1Fps ds 1
msu1FrameCount ds 2
msu1CurrentFrame ds 2
msu1CurrentFramePointer ds 4
msu1CurrentTrack db
msu1VideoPlaying db

msu1PaletteLength dw
msu1TilemapLength dw
msu1TilesLength dw
msu1Framebuffer INSTANCEOF oopObjHash MSU1.FRAMEBUFFER.COUNT
msu1CurrentFramebuffer INSTANCEOF oopObjHash
msu1CurrentStart dw
msu1CurrentLength dw
*/
zpLen ds 0
.ende

;object class static flags, default properties and zero page 
.define CLASS.FLAGS (OBJECT.FLAGS.Present | OBJECT.FLAGS.Singleton)
.define CLASS.PROPERTIES 0
.define CLASS.ZP_LENGTH zpLen

.ramsection "global msu1 vars" bank 0 slot 1
MSU1.GLOBAL.START ds 0

GLOBAL.currentFrame dw
GLOBAL.videoPlaying db

MSU1.GLOBAL.END ds 0
.ends

.base BSL
.bank 0 slot 0
/*.section "msu1Dat"
	OOPOBJ Msu1 $81 zpLen playVideo stopVideo getCurrentFrame
.ends*/


.Section "msu1HardwareString" superfree
msu1HardwareIdentifier:
	.db "S-MSU1"
msu1HardwareIdentifier.end:
.ends

