.include "src/config/config.inc"

.base REGS
;direct page global defines ram $00:0000-$00:1fff
.ramsection "stack buffr" bank 0 slot 2
STACK_strt ds $120
STACK db
STACK_end dw
.ends

.ramsection "zeropage vars" bank 0 slot 2
ZP ds kernelEnd-kernelStart
.ends

.ramsection "global vars" bank 0 slot 2
VARS									ds 0
SnesIrqFlags					db
Sa1IrqFlags						db
OopObjCount						dw	;counts how many times createoopobj was called. used to generate fingerprint
rendererIrqPTR INSTANCEOF oopObjHash
rendererFrame					dw
rendererScene					dw
charConvReady 				db	;0=wait, 1=ready
GLOBAL.memsel	db
VARS_end							ds 0
.ends


.base BSL