.include "src/config/config.inc"

.struct vars
  score dw
  name ds 4
  lifes db
.endst

;zp-vars
.enum 0
  iterator INSTANCEOF iteratorStruct
  this INSTANCEOF vars

zpLen ds 0
.ende

.define sort.score.score this.score
.export sort.score.score

;object class static flags, default properties and zero page 
.define CLASS.FLAGS OBJECT.FLAGS.Present
.define CLASS.PROPERTIES OBJECT.PROPERTIES.isSerializable
.define CLASS.ZP_LENGTH zpLen


.base BSL
.bank 0 slot 0
