.include "src/config/config.inc"


.def SRAM.BASE $206000
.def SRAM.SIGNATURE.VALUE $1337
.def SRAM.SLOT.SIGNATURE.VALUE $1338
.def SRAM.SIGNATURE.POST.VALUE $1339
.def SRAM.TEST.VALUE.0 $aaaa
.def SRAM.TEST.VALUE.1 $5555


.enum 0
  SRAM.SIGNATURE dw
  SRAM.LENGTH dw
  SRAM.CHSUM db
  SRAM.CHSUM.XOR db
  SRAM.SLOTS dw
.ende

.enum 0
  SRAM.SLOT.SIGNATURE dw
  SRAM.SLOT.OBJECT_ID dw
  SRAM.SLOT.SIZE db

.ende
/*
;ram buffers
.ramsection "global persistency vars" bank 0 slot 1
PERSISTENCY.GLOBAL.START ds 0
GLOBAL.persistency.sram.pointer ds 3
GLOBAL.persistency.checksum dw
GLOBAL.persistency.object.id db
GLOBAL.persistency.object.length db
GLOBAL.persistency.class.pointer db

PERSISTENCY.GLOBAL.END ds 0
.ends
*/
.struct vars
  target.properties dw
  sram.pointer ds 3
  sram.length dw
  checksum dw
  object.id db
  object.length dw  
  class.pointer ds 3
.endst

;zp-vars
.enum 0
  iterator INSTANCEOF iteratorStruct
  this INSTANCEOF vars

zpLen ds 0
.ende

.ramsection "persistency zero page" bank 0 slot 2
core.persistency.zp.start ds zpLen
core.persistency.zp.end ds 0
.ends

.base BSL
.bank 0 slot 0
