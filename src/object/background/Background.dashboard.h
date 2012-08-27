.include "src/config/config.inc"

/*.def DASHBOARD.IRQ.X 260
.def DASHBOARD.IRQ.Y 164-33*/

.def DASHBOARD.DISPLACEMENT.Y 164-33

.struct vars
  bg db
  irq.x dw
  irq.y dw
  hdma.mode ds 4
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
.define CLASS.PROPERTIES OBJECT.PROPERTIES.isDash
.define CLASS.ZP_LENGTH zpLen
.define CLASS.IMPLEMENTS interface.dimension

.ramsection "global vars dashboard" bank 0 slot 1
GLOBAL.dashboard.mode   db
GLOBAL.dashboard.mainScreen   db
GLOBAL.dashboard.subScreen   db
GLOBAL.dashboard.tileMap   dw
GLOBAL.dashboard.tiles   dw
GLOBAL.dashboard.position.x   dw
GLOBAL.dashboard.position.y   dw
.ends


.base BSL
.bank 0 slot 0

