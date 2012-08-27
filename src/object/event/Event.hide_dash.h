.include "src/config/config.inc"

;zp-vars
.enum 0
  iterator INSTANCEOF iteratorStruct
  event INSTANCEOF eventStruct
  zpLen ds 0
.ende

;.def HIDE_DASH.DISTANCE 80 << 8
.def HIDE_DASH.DISTANCE 60 << 8

;object class static flags, default properties and zero page 
.define CLASS.FLAGS OBJECT.FLAGS.Present
.define CLASS.PROPERTIES OBJECT.PROPERTIES.isEvent
.define CLASS.ZP_LENGTH zpLen

.base BSL
.bank 0 slot 0


