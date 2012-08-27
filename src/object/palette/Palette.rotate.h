.include "src/config/config.inc"

.struct palStruct
  delay dw
  decay dw
  counter dw
  current db
  target db
  inited dw
.endst

;zp-vars
.enum 0
  iterator INSTANCEOF iteratorStruct
  palette INSTANCEOF paletteStruct
  this INSTANCEOF palStruct

zpLen ds 0
.ende

;object class static flags, default properties and zero page 
.define CLASS.FLAGS OBJECT.FLAGS.Present
.define CLASS.PROPERTIES 0
.define CLASS.ZP_LENGTH zpLen


.base BSL
.bank 0 slot 0
