.include "src/config/config.inc"

.def INPUT.DEVICE.COUNT 1
/*
.enum 0
  INPUT.DEVICE.TYPE.NONE db
  INPUT.DEVICE.TYPE.JOYPAD db
.ende
*/
.enum 0 export
  INPUT.DEVICE.ID.0 db
/*  INPUT.DEVICE.ID.1 db
  INPUT.DEVICE.ID.2 db
  INPUT.DEVICE.ID.3 db*/
  INPUT.DEVICE.ID.MAX ds 0
.ende

.struct input
  press dw
  trigger dw
  mask dw
  old dw
.endst
		 
.ramsection "global.input" bank 0 slot 1
  CheckJoypadMode	db
  inputDevice INSTANCEOF input INPUT.DEVICE.COUNT
.ends

.base BSL

