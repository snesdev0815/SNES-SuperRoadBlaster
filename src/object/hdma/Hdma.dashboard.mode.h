.include "src/config/config.inc"

;defines
.def HDMA.DASHBOARD.MODE.CHANNEL.COUNT 5
.def HDMA.DASHBOARD.MODE.CHANNEL.LENGTH _sizeof_hdmaStruct

.struct vars
  buffer.cgwsel db
  position dw
  current.channel dw
  current.target dw
  current.register.pre dw
  current.register.post dw
  ramBuffer.start dw
  ramBuffer.id dw
  ramBuffer.length dw
.endst
		 
;zp-vars
.enum 0
  iterator INSTANCEOF iteratorStruct
  hdma INSTANCEOF hdmaStruct
  hdma.mode INSTANCEOF hdmaStruct
  hdma.mainScreen INSTANCEOF hdmaStruct
  hdma.tileMap INSTANCEOF hdmaStruct
  hdma.tiles INSTANCEOF hdmaStruct
  hdma.position INSTANCEOF hdmaStruct
  this INSTANCEOF vars
zpLen ds 0
.ende

;object class static flags, default properties and zero page 
.define CLASS.FLAGS OBJECT.FLAGS.Present
.define CLASS.PROPERTIES OBJECT.PROPERTIES.isHdma
.define CLASS.ZP_LENGTH zpLen

.base BSL
.bank 0 slot 0



