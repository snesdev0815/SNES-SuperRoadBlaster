.include "src/config/config.inc"

;defines
.def DMA_CHANNELS.COUNT 8

;structs:
.struct dmaQueue
  entry db	;nonzero if channel allocated
.endst


;ram buffers
.ramsection "global dma_channel vars" bank 0 slot 1
GLOBAL.DMA_CHANNELS.START ds 0
GLOBAL.DMA_CHANNELS INSTANCEOF dmaQueue DMA_CHANNELS.COUNT
GLOBAL.DMA_CHANNELS.END ds 0
.ends

.base BSL
.bank 0 slot 0
