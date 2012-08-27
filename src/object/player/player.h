.include "src/config/config.inc"

.def PLAYER.LIFES.DEFAULT 5
		 
.struct playerStruct
  score dw
  name ds 4
  lifes db
  noMiss db
.endst

;zp-vars
.enum 0
  iterator INSTANCEOF iteratorStruct
  this INSTANCEOF playerStruct

zpLen ds 0
.ende

;object class static flags, default properties and zero page 
.define CLASS.FLAGS (OBJECT.FLAGS.Present | OBJECT.FLAGS.Singleton)
.define CLASS.PROPERTIES 0
.define CLASS.ZP_LENGTH zpLen


.base BSL
.bank 0 slot 0
