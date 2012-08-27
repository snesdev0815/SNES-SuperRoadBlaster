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
/*
  .db $01, $02, $02, $03, $04, $04, $05, $06, $06, $07, $07, $07, $08, $08, $08, $08
  .db $68, $85, $d2, $e2, $20, $a9, $01, $8d, $00, $42, $a9, $8f, $8d, $00, $21, $9c
  .db $0c, $42, $c2, $20, $a9, $00, $01, $85, $d7, $a9, $01, $06, $85, $d6, $a9, $c0
  .db $00, $8d, $1a, $21, $a9, $12, $00, $20, $29, $dd, $9c, $16, $21, $a2, $00, $00
  .db $bf, $00, $20, $7e, $85, $c2, $e2, $20, $a0, $08, $00, $a9, $00, $06, $c3, $2a
*/
  .db $08, $08, $08, $08, $07, $07, $07, $06, $06, $05, $04, $04, $03, $02, $02, $01
  .db $00, $ff, $fe, $fe, $fd, $fc, $fc, $fb, $fa, $fa, $f9, $f9, $f9, $f8, $f8, $f8
  .db $f8, $f8, $f8, $f9, $f9, $f9, $fa, $fa, $fb, $fc, $fc, $fd, $fe, $fe, $ff, $00
  .db $01, $02, $02, $03, $04, $04, $05, $06, $06, $07, $07, $07, $08, $08, $08, $08

.ends