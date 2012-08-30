.include "src/config/config.inc"

.def LOGO_ZOOM.TABLE.LENGTH $300		 
		 
.struct vars
  tableEnd dw
  tablePointer dw
  lutPointer dw
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


.section "logoZoomInitLUT" superfree
logoZoomInitLUT:
  .db $08, $08, $08, $08, $07, $07, $07, $06, $06, $05, $04, $04, $03, $02, $02, $01
  .db $00, $ff, $fe, $fe, $fd, $fc, $fc, $fb, $fa, $fa, $f9, $f9, $f9, $f8, $f8, $f8
  .db $f8, $f8, $f8, $f9, $f9, $f9, $fa, $fa, $fb, $fc, $fc, $fd, $fe, $fe, $ff, $00
  .db $01, $02, $02, $03, $04, $04, $05, $06, $06, $07, $07, $07, $08, $08, $08, $08

.ends