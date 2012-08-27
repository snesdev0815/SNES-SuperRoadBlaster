.include "src/config/config.inc"

.def SPRITE.LIFE_CAR.MAXAGE 120

.struct vars
  spriteMap.upperLeft dw
  spriteMap.upperRight dw
  spriteMap.lowerLeft dw
  spriteMap.lowerRight dw  
  player ds 4
  speed dw
  accel dw
  age dw
  lifes dw
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
.define CLASS.FLAGS OBJECT.FLAGS.Present
.define CLASS.PROPERTIES OBJECT.PROPERTIES.isSprite
.define CLASS.ZP_LENGTH zpLen
.define CLASS.IMPLEMENTS interface.dimension

.base BSL
.bank 0 slot 0

