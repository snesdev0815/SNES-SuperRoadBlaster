.include "src/config/config.inc"

.struct zp
  delta.x dw
  delta.y dw
  age dw
.endst

;zp-vars
.enum 0
  iterator INSTANCEOF iteratorStruct
  event INSTANCEOF eventStruct
  this INSTANCEOF zp
  zpLen ds 0
.ende


;object class static flags, default properties and zero page 
.define CLASS.FLAGS OBJECT.FLAGS.Present
.define CLASS.PROPERTIES OBJECT.PROPERTIES.isEvent
.define CLASS.ZP_LENGTH zpLen

.base BSL
.bank 0 slot 0

.section "Event.shake.LUT" superfree

Event.shake.LUT:
  .db 5, -5, 5, -5, 5, -5, 5, -5, 4, -4, 4, -4, 4, -4,
  .db 4, -4, 3, -3, 3, -3, 3, -3, 3, -3, 3, -3, 3, -3, 3, -3, 3, -3, 3, -3
  .db 2, -2, 2, -2, 2, -2, 1, -1, 1, -1, 0, 1, -1, 0, 0, 0, 1, -1,
Event.shake.LUT.end:

.ends