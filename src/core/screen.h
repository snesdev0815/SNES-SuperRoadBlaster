.include "src/config/config.inc"

;defines
.def SCREEN.DEFAULT.SIZE.X = $ff
.def SCREEN.DEFAULT.SIZE.Y = $df
.export SCREEN.DEFAULT.SIZE.X
.export SCREEN.DEFAULT.SIZE.Y

;ram buffers
.ramsection "global dmafifo vars" bank 0 slot 1
SCREEN.GLOBAL.START ds 0

GLOBAL.screen.position.x dw
GLOBAL.screen.position.y dw
GLOBAL.screen.size.x dw
GLOBAL.screen.size.y dw

SCREEN.GLOBAL.END ds 0
.ends

.base BSL
.bank 0 slot 0
