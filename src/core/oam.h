.include "src/config/config.inc"

;defines
.def OAM_SLOTS 128

.def OAM.TABLE.0.START 0
.def OAM.TABLE.0.LENGTH $200
.def OAM.TABLE.1.START $200
.def OAM.TABLE.1.LENGTH $20

;structs:
.struct oamSlot	;must be 8 bytes in length
  x	db
  y db
  tile db
  flags db
.endst


;ram buffers
.ramsection "global dmafifo vars" bank 0 slot 1
OAM.GLOBAL.START ds 0

GLOBAL.currentOamSlot dw
GLOBAL.oamUploadFlag db
GLOBAL.oamClearFlag db
GLOBAL.oamBuffer INSTANCEOF oamSlot OAM_SLOTS
GLOBAL.oamBuffer.end ds 0
GLOBAL.oam.vram.id db
GLOBAL.oam.vram.start dw

OAM.GLOBAL.END ds 0
.ends

.base BSL
.bank 0 slot 0
