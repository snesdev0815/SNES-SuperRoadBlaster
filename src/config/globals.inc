.include "src/definition/snes.registers"
.include "src/definition/msu1.registers"
.include "src/config/macros.inc"
.include "src/config/structs.inc"

;kernel zp-vars(used by init,memoryclear,oophandler etc)
.enum 0
kernelStart ds 0

tmp					ds 32
dpBuffr			dw
stackBuffr	dw
errCurr			db
classCurr		db
routCurr		db
OopObjSlotPtr dw	;current position in obj-entry buffer
OopObjRamPtr dw	;current fill position in obj ram block
kernelEnd 	ds 0
.ende

;global defines
.enum 5
OBJECT.CALL.ARG.8	dw
OBJECT.CALL.ARG.7	dw
OBJECT.CALL.ARG.6	dw
OBJECT.CALL.ARG.5	dw
OBJECT.CALL.ARG.4	dw
OBJECT.CALL.ARG.3	dw
OBJECT.CALL.ARG.2	dw
OBJECT.CALL.ARG.1	dw
;OBJECT.CALL.ARG.0	dw ;this is a
.ende

;object status flags
.def OBJECT.FLAGS.Singleton	1 << 0
.def OBJECT.FLAGS.Persistent	1 << 1
.def OBJECT.FLAGS.InitOk	1 << 2
.def OBJECT.FLAGS.DeleteScheduled	1 << 3
.def OBJECT.FLAGS.Present	1 << 7

;obj properties (word)
.def OBJECT.PROPERTIES.isScript	1 << 0
.def OBJECT.PROPERTIES.isChapter	1 << 1
.def OBJECT.PROPERTIES.isEvent	1 << 2
.def OBJECT.PROPERTIES.isHdma	1 << 3
.def OBJECT.PROPERTIES.isCollidable	1 << 4
.def OBJECT.PROPERTIES.isLifeform	1 << 5
.def OBJECT.PROPERTIES.isUnitTest	1 << 6
.def OBJECT.PROPERTIES.likesBananas	1 << 7
.def OBJECT.PROPERTIES.likesHamburgers	1 << 8
.def OBJECT.PROPERTIES.isCheckpoint	1 << 9
.def OBJECT.PROPERTIES.isSprite	1 << 10
.def OBJECT.PROPERTIES.isDash	1 << 11
.def OBJECT.PROPERTIES.isSerializable	1 << 12
.def OBJECT.PROPERTIES.isHud   1 << 13



.enum 0
MALLOC.TILES db
MALLOC.TILEMAP db
MALLOC.PALETTE db
MALLOC.MAXTYPES ds 0
.ende

.enum 0
PALETTE.BPP.1 db
PALETTE.BPP.2 db
PALETTE.BPP.4 db
PALETTE.BPP.8 db
.ende

.enum 0
BG.LAYER.0 db
BG.LAYER.1 db
BG.LAYER.2 db
BG.LAYER.3 db
.ende


.enum 0
EventTarget.none db
.ende

;animation file format (sprites and bgs)
.enum 0
  ANIMATION.MAGIC dw
  ANIMATION.MAX.TILES dw
  ANIMATION.MAX.PALETTE dw
  ANIMATION.MAX.FRAMES dw
  ANIMATION.BPP db
  ANIMATION.FRAME.POINTER dw
.ende

.enum 0
  ANIMATION.FRAME.TILES.LENGTH dw
  ANIMATION.FRAME.TILEMAP.LENGTH dw  
  ANIMATION.FRAME.PALETTE.LENGTH dw
  ANIMATION.FRAME.DATA dw
.ende
;wla dx is too stupid to use this as a word value, so this hack has to do
;.def ANIMATION.MAGIC.VALUE "SP"
.def ANIMATION.MAGIC.VALUE $5053


;interfaces
.enum 0
interface.dimension db
.ende


.def PALETTE.COLOR.COUNT 256
.def PALETTE.COLOR.SIZE 2
.def PALETTE.START.BG 0
.def PALETTE.START.SPRITE $100
.def PALETTE.START.SPRITE_COLORMATH $180
.def PALETTE.GRANULARITY.1BPP $4
.def PALETTE.GRANULARITY.2BPP $8
.def PALETTE.GRANULARITY.4BPP $20
.def PALETTE.GRANULARITY.8BPP $200


.def TILEMAP.GRANULARITY $800
.def TILEMAP.SIZE.SINGLE $800
.def TILEMAP.SIZE.DUAL $1000
.def TILEMAP.SIZE.QUADRUPLE $2000

.def TILES.GRANULARITY $2000

.def SPRITE.NAMETABLE.GRANULARITY $4000
;.def SPRITE.NAMETABLE.PRIMER SPRITE.NAMETABLE.GRANULARITY * 3
.def SPRITE.NAMETABLE.PRIMER $c000
.def SPRITE.TILE.GRANULARITY $100

.def PLAYER.BONUS.DEFAULT 1
.def PLAYER.BONUS.EXTRA 2

.def EVENT.BONUS.EXTRA.TIMEOUT 16

;program-specific stuff
.define TILE2BPP	16
.define TILE4BPP	32
.define TILE8BPP	64

.define frameResX 32
.define frameResY 15

.define rwTest	$aa55

.define oopCreateNoPtr $ffff

.define TRUE	1
.define FALSE	0

.def SCRIPT_MAGIC $bade
.def RESULT_MAGIC $affe
.def IRQ_MAGIC $dead

.def SCRIPT.MAX_AGE.DEFAULT $80

.def SPRITE.LIFE_COUNTER.MAX_AGE 120

.enum 0
WRAM.CLEAR_PATTERN.ZERO db
WRAM.CLEAR_PATTERN.NOP db
WRAM.CLEAR_PATTERN.BG3 db
WRAM.CLEAR_PATTERN.OAM db
WRAM.CLEAR_PATTERN.BG1 db
WRAM.CLEAR_PATTERN.STRING db
.ende

.def BRIGHTNESS.FULL $f
.def BRIGHTNESS.HALF $8
.def BRIGHTNESS.NONE $0

.def HIGHSCORE.COUNT 5

.def IRQ.VPOS.PAL 191
.def IRQ.VPOS.NTSC 186

;memory clear patterns
.def MEMORY_CLEAR.ZERO 0
.def MEMORY_CLEAR.NOP $eaea
.def MEMORY_CLEAR.TILEMAP.BG1 $2907
.def MEMORY_CLEAR.TILEMAP.BG3 $2400
.def MEMORY_CLEAR.OAM $00f8
.def MEMORY_CLEAR.STRING $2020
/*
    .dw 0           ;zeros
    .dw $eaea       ;nops
    .dw $2400       ;bg3 tilemap clear word
    .dw $00f8       ;oam buffer
    .dw $2907       ;bg1 tilemap clear
    .dw $2020       ;string buffer
*/