.include "src/config/config.inc"


.def BG.PALETTE.BITS %11100

;this is a hack, should be defined in animation file instead
.def BG.TILEMAP.LENGTH $800
.export BG.TILEMAP.LENGTH

;zp-vars,just a reference
.enum 0
  iterator INSTANCEOF iteratorStruct
  dimension INSTANCEOF dimensionStruct
  animation INSTANCEOF animationStruct
zpLen ds 0
.ende

;object class static flags, default properties and zero page 
.define CLASS.FLAGS OBJECT.FLAGS.Present
.define CLASS.PROPERTIES 0
.define CLASS.ZP_LENGTH zpLen
.define CLASS.IMPLEMENTS interface.dimension

.base BSL
.bank 0 slot 0

.section "BgBitflagLUT" superfree
BgBitflagLUT:
  .db T_BG1_ENABLE
  .db T_BG2_ENABLE
  .db T_BG3_ENABLE
  .db T_BG4_ENABLE
.ends

.section "palette_granularity_lut" superfree
PALETTE.GRANULARITY.LUT:
  .dw PALETTE.GRANULARITY.1BPP
  .dw PALETTE.GRANULARITY.2BPP
  .dw PALETTE.GRANULARITY.4BPP
  .dw PALETTE.GRANULARITY.8BPP
  .dw PALETTE.GRANULARITY.8BPP
.ends

.section "tilemap_length_lut" superfree
TILEMAP.LENGTH.LUT:
  .dw TILEMAP.SIZE.SINGLE
  .dw TILEMAP.SIZE.DUAL
  .dw TILEMAP.SIZE.DUAL
  .dw TILEMAP.SIZE.QUADRUPLE
.ends

.section "tiles_mask_lut" superfree
TILES.MASK.LUT:
  .dw $fff0
  .dw $ff0f
  .dw $f0ff
  .dw $0fff
.ends

.section "tiles_shift_lut" superfree
TILES.SHIFT.LUT:
  .dw 0
  .dw 4
  .dw 8
  .dw 12
.ends

.Section "BackgroundAnimationLUT" superfree
BackgroundAnimationLUT:
  PTRLONG BackgroundAnimationLUT BG.msu1
  PTRLONG BackgroundAnimationLUT BG.titlescreen
  PTRLONG BackgroundAnimationLUT BG.logo
  PTRLONG BackgroundAnimationLUT BG.hiscore
  PTRLONG BackgroundAnimationLUT BG.scoreentry
  PTRLONG BackgroundAnimationLUT BG.hud
;  PTRLONG BackgroundAnimationLUT BG.levelcomplete.0
  PTRLONG BackgroundAnimationLUT BG.levelcomplete.1
  PTRLONG BackgroundAnimationLUT BG.levelcomplete.2
  
.ends
  BG_ANIMATION msu1 gfx_bg
  BG_ANIMATION titlescreen gfx_bg
  BG_ANIMATION logo gfx_bg
  BG_ANIMATION hiscore gfx_bg
  BG_ANIMATION scoreentry gfx_bg
  BG_ANIMATION hud gfx_directcolor
;  BG_ANIMATION levelcomplete.0 gfx_bg
  BG_ANIMATION levelcomplete.1 gfx_bg
  BG_ANIMATION levelcomplete.2 gfx_bg  

