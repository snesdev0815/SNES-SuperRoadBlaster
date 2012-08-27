.include "src/config/config.inc"

.def IRQ.POSITION.Y.MAX 224


.ramsection "global vars irq" bank 0 slot 1
GLOBAL.irq.xpos   dw
GLOBAL.irq.ypos   dw
GLOBAL.irq.callback   dw
GLOBAL.irq.buffer ds 16
.ends


.base BSL
