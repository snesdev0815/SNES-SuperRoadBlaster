.include "src/config/config.inc"

.struct zpVars
  tmp ds 8
  selfTest dw
.endst


;zp-vars
.enum 0
  iterator INSTANCEOF iteratorStruct
  this INSTANCEOF zpVars 
  hashPtr INSTANCEOF oopObjHash 4
  zpLen ds 0
.ende


;object class static flags, default properties and zero page 
.define CLASS.FLAGS (OBJECT.FLAGS.Present | OBJECT.FLAGS.Singleton)
.define CLASS.PROPERTIES OBJECT.PROPERTIES.isUnitTest
.define CLASS.ZP_LENGTH zpLen

.base BSL
.bank 0 slot 0



