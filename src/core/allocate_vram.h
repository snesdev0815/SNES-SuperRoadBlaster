.include "src/config/config.inc"

;defines
.def VRAM_ALLOCATION_BLOCKSIZE $100
.def VRAM_ALLOCATION_BLOCKS $100

.def VRAM_ALLOCATION_STEP.MIN VRAM_ALLOCATION_BLOCKSIZE
.def VRAM_ALLOCATION_STEP.MAX $4000


;ram buffers
.ramsection "global vram_allocate vars" bank 0 slot 1
VRAM_ALLOCATE.GLOBAL.START ds 0
GLOBAL.currentVramAllocationId db
GLOBAL.vramAllocation.input.stepsize dw
GLOBAL.vramAllocation.input.length dw
GLOBAL.vramAllocation.input.grantId dw
GLOBAL.vramAllocation.temp.start dw
GLOBAL.vramAllocation.temp.length dw
GLOBAL.vramAllocationBlocks ds VRAM_ALLOCATION_BLOCKS
VRAM_ALLOCATE.GLOBAL.END ds 0
.ends

.base BSL
.bank 0 slot 0
