.include "src/config/config.inc"

.struct vars
  _tmp ds 8
  checkPointAdress dw
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
.define CLASS.PROPERTIES OBJECT.PROPERTIES.isCheckpoint
.define CLASS.ZP_LENGTH zpLen

.base BSL
.bank 0 slot 0


