.include "src/config/config.inc"


;zp-vars
.enum 0
  iterator INSTANCEOF iteratorStruct
  _tmp ds 8
  zpLen ds 0
.ende

;object class static flags, default properties and zero page 
.define CLASS.FLAGS OBJECT.FLAGS.Present
.define CLASS.PROPERTIES (OBJECT.PROPERTIES.isUnitTest | OBJECT.PROPERTIES.isLifeform)
.define CLASS.ZP_LENGTH zpLen

.base BSL
.bank 0 slot 0




