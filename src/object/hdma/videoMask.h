.include "src/config/config.inc"

.struct vars
  buffer.window12Sel db
  buffer.windowObjSel db
  buffer.windowMainscreen db
.endst
		 
;zp-vars
.enum 0
  iterator INSTANCEOF iteratorStruct
  hdma INSTANCEOF hdmaStruct
  this INSTANCEOF vars
zpLen ds 0
.ende

;object class static flags, default properties and zero page 
.define CLASS.FLAGS OBJECT.FLAGS.Present
.define CLASS.PROPERTIES OBJECT.PROPERTIES.isHdma
.define CLASS.ZP_LENGTH zpLen

.base BSL
.bank 0 slot 0

.section "VideoMaskTable.pal" superfree

;direct, goes to W1L, W1R (window 1 position)
VideoMaskTable.pal:
  .db $20
	.db $00
	.db $ff
  .db $01
	.db $01	;negative window range, disable
	.db $00
  .db $00

.ends

.section "VideoMaskTable.ntsc" superfree
  
VideoMaskTable.ntsc:
  .db $25
    .db $00
    .db $ff
  .db $01
    .db $01 ;negative window range, disable
    .db $00
  .db $00
  
.ends

