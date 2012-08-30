.include "src/config/config.inc"
		 
;zp-vars
.enum 0
  iterator INSTANCEOF iteratorStruct
  script INSTANCEOF scriptStruct
  this INSTANCEOF scriptStruct
  zpLen ds 0
.ende


  
;object class static flags, default properties and zero page 
.define CLASS.FLAGS OBJECT.FLAGS.Present
.define CLASS.PROPERTIES OBJECT.PROPERTIES.isEvent
.define CLASS.ZP_LENGTH zpLen

.base BSL
.bank 0 slot 0


