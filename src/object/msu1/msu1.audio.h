.include "src/config/config.inc"


.define MSU1_SEEK_TIMEOUT $2000
.define MSU1_FILE.TITLE.LEN 21

.struct MSU1_FILE
  ID	ds 6
  TITLE ds 21
  BPP db
  FPS db
  CHAPTERCOUNT db
  CHECKSUM ds 2
  POINTER ds 4
.endst

.struct vars
  currentTrack db
  audioPlaying db
.endst

;zp-vars
.enum 0
  iterator INSTANCEOF iteratorStruct
  this INSTANCEOF vars

zpLen ds 0
.ende

;object class static flags, default properties and zero page 
.define CLASS.FLAGS (OBJECT.FLAGS.Present | OBJECT.FLAGS.Singleton)
.define CLASS.PROPERTIES 0
.define CLASS.ZP_LENGTH zpLen
/*
.ramsection "global msu1 vars" bank 0 slot 1
MSU1.GLOBAL.START ds 0

GLOBAL.currentFrame dw
GLOBAL.videoPlaying db

MSU1.GLOBAL.END ds 0
.ends
*/
.base BSL
.bank 0 slot 0
/*.section "msu1Dat"
	OOPOBJ Msu1 $81 zpLen playVideo stopVideo getCurrentFrame
.ends*/



