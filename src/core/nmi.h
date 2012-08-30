.include "src/config/config.inc"

.ramsection "global vars nmi" bank 0 slot 1
NmiGlobalVarsStrt ds 0

SetIni	db
window12Sel	db
window1Left	db
window2Left	db
windowBGLogic	db
windowMainscreen	db
windowObjSel	db
mosaicSetting	db
ScreenMode db
MainScreen db
SubScreen db
BGTilesVram12 db
BGTilesVram34 db
BG1TilemapVram db
BG2TilemapVram db
BG3TilemapVram db
BG4TilemapVram db
colorAdditionSelect db
CgadsubConfig db
FixedColourB db
FixedColourG db
FixedColourR db
xScrollBG1 dw
yScrollBG1 dw
xScrollBG2 dw
yScrollBG2 dw
xScrollBG3 dw
yScrollBG3 dw
xScrollBG4 dw
yScrollBG4 dw
ObjSel db

;buffers that change only once at start of frame - for indirect hdma
GLOBAL.BUFFER.screenMode db
GLOBAL.BUFFER.mainScreen db
GLOBAL.BUFFER.subScreen db
GLOBALS.BUFFER.bg1Tilemap db
GLOBALS.BUFFER.bg12Tiles db
GLOBALS.BUFFER.scroll.bg1.x dw
GLOBALS.BUFFER.scroll.bg1.y dw

GLOBAL.HDMA.CHANNEL.ENABLE db

FrameCounter	dw
LastFrame		dw

FrameClipStart db
FrameClipEnd db

CpuUsageScanline			db
ScreenBrightness 			db
GLOBAL.interruptFlags	db

irqCount		dw
dmaIrqCount	dw
frameIrqCount dw
frameBuffHistory ds 3
irqCheckpoint db

NmiGlobalVarsEnd ds 0
.ends


.base BSL
.bank 0 slot 0
