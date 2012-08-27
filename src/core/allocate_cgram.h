.include "src/config/config.inc"

;defines
.def CGRAM_ALLOCATION_BLOCKSIZE $8
.def CGRAM_ALLOCATION_BLOCKS PALETTE.COLOR.COUNT * PALETTE.COLOR.SIZE / CGRAM_ALLOCATION_BLOCKSIZE

.def CGRAM_ALLOCATION_STEP.MIN CGRAM_ALLOCATION_BLOCKSIZE
.def CGRAM_ALLOCATION_STEP.MAX $200

;ram buffers
.ramsection "global cgram_allocate vars" bank 0 slot 1
CGRAM_ALLOCATE.GLOBAL.START ds 0
GLOBAL.currentCgramAllocationId db
GLOBAL.cgramAllocation.input.stepsize dw
GLOBAL.cgramAllocation.input.length dw
GLOBAL.cgramAllocation.input.start dw
GLOBAL.cgramAllocation.temp.start dw
GLOBAL.cgramAllocation.temp.length dw
GLOBAL.cgramAllocation.max.length dw
GLOBAL.cgramAllocationBlocks ds CGRAM_ALLOCATION_BLOCKS
CGRAM_ALLOCATE.GLOBAL.END ds 0
.ends

.base BSL
.bank 0 slot 0
