.include "src/config/config.inc"

;defines
.def NumOfHashptr 9


.struct vars
  _tmp ds 16
  currPC	dw	;current exec address in script
  buffFlags db	;flags.
  buffBank db		;bank. unused, just for convenience
  buffA	dw
  buffX	dw
  buffY	dw
  buffStack dw	;used to check for stack trashes
.endst
		 
;zp-vars
.enum 0
  iterator INSTANCEOF iteratorStruct
  script INSTANCEOF scriptStruct
  this INSTANCEOF vars
  hashPtr INSTANCEOF oopObjHash NumOfHashptr  
  zpLen ds 0
.ende


;object class static flags, default properties and zero page 
.define CLASS.FLAGS OBJECT.FLAGS.Present
.define CLASS.PROPERTIES OBJECT.PROPERTIES.isScript
.define CLASS.ZP_LENGTH zpLen


.base BSL
.bank 0 slot 0

.section "scripts"

.include "src/main.script"
.include "src/none.script"
.include "src/title_screen.script"
.include "src/hall_of_fame.script"
.include "src/msu1.script"
.include "src/score_entry.script"
.include "src/level_complete.script"
.include "data/chapters/chapter.include"

.ends
