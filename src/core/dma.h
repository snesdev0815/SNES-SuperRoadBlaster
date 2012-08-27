.include "src/config/config.inc"

;defines
.def DMA_QUEUE_SLOTS 16	;must be power of two
.def TRANSFER_ACTIVE $8000

;dma transfer types
.enum 0 export
DMA_TRANSFER.VRAM	db
DMA_TRANSFER.OAM	db
DMA_TRANSFER.CGRAM	db
DMA_TRANSFER.MAX ds 0
.ende

.def DMA_TRANSFER.OPTION.FIXED_SOURCE $80
.def DMA_TRANSFER.OPTION.ACTIVE $40
.def DMA_TRANSFER.OPTION.REVERSE $20    ;switch transfer direction, b-bus to a-bus

.export DMA_TRANSFER.OPTION.FIXED_SOURCE
.export DMA_TRANSFER.OPTION.REVERSE
;structs:
.struct dmaQueue	;must be 8 bytes in length
  transferLength dw
  targetAdress dw
  transferType db
  sourceAdress ds 3
.endst


;ram buffers
.ramsection "global dmafifo vars" bank 0 slot 1
DMA_QUEUE.GLOBAL.START ds 0

GLOBAL.currentDmaQueueSlot db
GLOBAL.dmaQueueChannel.id db
GLOBAL.dmaQueueChannel.flag db
GLOBAL.dmaQueueChannel.index dw
GLOBAL.dmaQueue INSTANCEOF dmaQueue DMA_QUEUE_SLOTS

DMA_QUEUE.GLOBAL.END ds 0
.ends

.base BSL
.bank 0 slot 0

.section "dmaQueueJumpLut" 
dmaQueueJumpTable:
  .dw dmaQueueVramTransfer
  .dw dmaQueueOamTransfer
  .dw dmaQueueCgramTransfer
.ends

.section "dmaBitflagLut" superfree
dmaBitflagLut:
    .db 1 << 0
    .db 1 << 1
    .db 1 << 2
    .db 1 << 3
    .db 1 << 4
    .db 1 << 5
    .db 1 << 6
    .db 1 << 7
.ends
