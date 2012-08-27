.include "src/config/config.inc"

.struct vars
  sprite ds 4
  audio ds 4
  age dw
.endst
		 
;zp-vars
.enum 0
  iterator INSTANCEOF iteratorStruct
  event INSTANCEOF eventStruct
  this INSTANCEOF vars
  zpLen ds 0
.ende

;object class static flags, default properties and zero page 
.define CLASS.FLAGS OBJECT.FLAGS.Present
.define CLASS.PROPERTIES OBJECT.PROPERTIES.isEvent
.define CLASS.ZP_LENGTH zpLen

.base BSL
.bank 0 slot 0

