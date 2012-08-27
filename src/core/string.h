.include "src/config/config.inc"


;defines

.def GLOBAL.CORE.STRING.buffer.lines 28
.def GLOBAL.CORE.STRING.buffer.columns 32
.def GLOBAL.CORE.STRING.buffer.length GLOBAL.CORE.STRING.buffer.lines * GLOBAL.CORE.STRING.buffer.columns
.export GLOBAL.CORE.STRING.buffer.length

;text string commands
.enum 0 export
TC_end	db		;terminate string
TC_sub	db		;print 0x00-terminated string, then return. 1 arg/1 byte: 16bit pointernumber(of stringpointer-LUT) to string
TC_iSub	db		;print 0x00-terminated string, then return. ;1 arg/2 bytes: 16bit pointer in bank $7e to 16bit pointernumber(of stringpointer-LUT) to string
TC_dSub	db		;print 0x00-terminated string, then return. ;1 arg/3 bytes: 24bit stringpointer
TC_diSub	db	;print 0x00-terminated string, then return. ;1 arg/2 bytes: 16bit pointer in bank $7e to 24bit string pointer
TC_pos	db		;set screen position, 1 arg/1 byte: tile position on screen
TC_brk	db		;linebreak, no arguments
TC_hToS	db		;print hex value. arg0,24bit:pointer to value. arg1,8bit: length(31 max)
TC_dToS	db		;print decimal value. arg0,24bit:pointer to value. arg1,8bit: length(3 max)
TC_max ds 0		;maximum command value
.ende

.enum 0
static.string.start ds 0
static.string INSTANCEOF static.string.struct
static.string.end ds 0
.ende


.ramsection "static string vars" bank 0 slot 2
directPage.static.string ds static.string.end - static.string.start
.ends


;ram buffers
.ramsection "global string vars" bank 0 slot 1
GLOBAL.CORE.STRING.START ds 0
  GLOBAL.CORE.STRING.argument.0 dw
  GLOBAL.CORE.STRING.argument.1 dw
  GLOBAL.CORE.STRING.argument.2 dw
  GLOBAL.CORE.STRING.argument.3 dw
  GLOBAL.CORE.STRING.buffer ds GLOBAL.CORE.STRING.buffer.length
GLOBAL.CORE.STRING.END ds 0
.ends

;data includes
.base BSL

.section "string command lut"
	ExcStrCmdLut:
		PTRNORM ExcStrCmdLut SUB_TC_end
		PTRNORM ExcStrCmdLut SUB_TC_sub
		PTRNORM ExcStrCmdLut SUB_TC_iSub
		PTRNORM ExcStrCmdLut SUB_TC_dSub
		PTRNORM ExcStrCmdLut SUB_TC_diSub
		PTRNORM ExcStrCmdLut SUB_TC_pos
		PTRNORM ExcStrCmdLut SUB_TC_brk
		PTRNORM ExcStrCmdLut SUB_TC_hToS
		PTRNORM ExcStrCmdLut SUB_TC_dToS
.ends

