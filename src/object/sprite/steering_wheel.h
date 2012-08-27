.include "src/config/config.inc"


.struct vars
  currentState dw
.endst
		 
;zp-vars
.enum 0
  iterator INSTANCEOF iteratorStruct
  dimension INSTANCEOF dimensionStruct
  animation INSTANCEOF animationStruct
  this INSTANCEOF vars
  zpLen ds 0
.ende

;object class static flags, default properties and zero page 
.define CLASS.FLAGS OBJECT.FLAGS.Present | OBJECT.FLAGS.Singleton
.define CLASS.PROPERTIES OBJECT.PROPERTIES.isSprite | OBJECT.PROPERTIES.isDash
.define CLASS.ZP_LENGTH zpLen
.define CLASS.IMPLEMENTS interface.dimension

.base BSL
.bank 0 slot 0
