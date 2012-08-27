.include "src/config/config.inc"


.def NAMEINPUT.LENGTH 3
.def NAMEINPUT.CHAR.START $30
.def NAMEINPUT.CHAR.END $5a
.def NAMEINPUT.CHAR.DEFAULT $41

.def NAMEINPUT.CURSOR.CHAR $20
.def NAMEINPUT.CURSOR.DELAY $1

.struct selfStruct
  name ds 4
  cursor.position db
  cursor.status db
  isDone db
.endst

;zp-vars
.enum 0
  iterator INSTANCEOF iteratorStruct
  this INSTANCEOF selfStruct

zpLen ds 0
.ende

;object class static flags, default properties and zero page 
.define CLASS.FLAGS OBJECT.FLAGS.Present
.define CLASS.PROPERTIES 0
.define CLASS.ZP_LENGTH zpLen


.base BSL
.bank 0 slot 0
