.include "src/config/config.inc"

.struct vars
    bg.dashboard ds 4
    sprite.dashboard ds 4
    sprite.steeringWheel ds 4
    hasDash dw 
    brightness ds 4
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


