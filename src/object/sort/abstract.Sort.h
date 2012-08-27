.include "src/config/config.inc"

;zp-vars,just a reference
.enum 0
  iterator INSTANCEOF iteratorStruct
zpLen ds 0
.ende

;object class static flags, default properties and zero page 
.define CLASS.FLAGS OBJECT.FLAGS.Present
.define CLASS.PROPERTIES 0
.define CLASS.ZP_LENGTH zpLen

.base BSL
.bank 0 slot 0
