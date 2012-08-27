.include "src/config/config.inc"

/*
.ramsection "oop obj ram zp" bank 0 slot 2

.ends
*/

;@todo, this is obsolete. should be merged with regular animation stuff
.struct backgroundStruct
  _tmp ds 8
  bpp	db
  bgNumber db
  tilemap.id db
  tilemap.start dw
  tilemap.length dw
  tilemap.mirrorFlags dw
  tiles.id db
  tiles.start dw
  tiles.length dw
  palette.id db
  palette.start dw
  palette.length dw
.endst


;zp-vars
.enum 0
  iterator INSTANCEOF iteratorStruct
  dimension INSTANCEOF dimensionStruct
  this INSTANCEOF backgroundStruct
  zpLen ds 0
.ende

;object class static flags, default properties and zero page 
.define CLASS.FLAGS OBJECT.FLAGS.Present
.define CLASS.PROPERTIES 0
.define CLASS.ZP_LENGTH zpLen
.define CLASS.IMPLEMENTS interface.dimension

.base BSL
.bank 0 slot 0



/*.section "backgroundDat"
	OOPOBJ Background $81 zpLen setX setY getAllocatedMemory
.ends*/

