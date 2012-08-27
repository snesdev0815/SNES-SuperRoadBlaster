.include "src/config/config.inc"

;ram buffers
.ramsection "global vram_allocate vars" bank 0 slot 1
RANDOM.GLOBAL.START ds 0

GLOBAL.random1	db
GLOBAL.random2	db
GLOBAL.random3	db
GLOBAL.random4	db

RANDOM.GLOBAL.END ds 0
.ends


.base BSL
.bank 0 slot 0
