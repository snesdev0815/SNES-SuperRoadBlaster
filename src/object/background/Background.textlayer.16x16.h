.include "src/config/config.inc"


.struct vars
  bg db
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
.define CLASS.PROPERTIES 0
.define CLASS.ZP_LENGTH zpLen
.define CLASS.IMPLEMENTS interface.dimension

.base BSL
.bank 0 slot 0

.section "16x16 font tiles" superfree
    FILEINC Font16x16Tiles "build/data/font/16x16.gfx_font4bpp.tiles"
.ends

.section "16x16 font pal" superfree
    FILEINC Font16x16Pal "build/data/font/16x16.gfx_font4bpp.palette"
.ends
