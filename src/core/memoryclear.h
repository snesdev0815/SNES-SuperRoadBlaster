.include "src/config/config.inc"

.base BSL
.section "clearPattern" superfree
;byte patterns to clear wram with.(8 entries max)   
;@see WRAM.CLEAR_PATTERN
ClearWramBytePatterns:
	.dw MEMORY_CLEAR.ZERO			;zeros
	.dw MEMORY_CLEAR.NOP		;nops
	.dw MEMORY_CLEAR.TILEMAP.BG3		;bg3 tilemap clear word
	.dw MEMORY_CLEAR.OAM		;oam buffer
	.dw MEMORY_CLEAR.TILEMAP.BG1		;bg1 tilemap clear
	.dw MEMORY_CLEAR.STRING		;string buffer
.ends