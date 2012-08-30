.include "src/config/config.inc"

.def OAM.PALETTE.BITS %1110

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

.Section "SpriteAnimationLUT" superfree
SpriteAnimationLUT:
  PTRLONG SpriteAnimationLUT SPRITE.right_arrow
  PTRLONG SpriteAnimationLUT SPRITE.left_arrow
  PTRLONG SpriteAnimationLUT SPRITE.turbo
  PTRLONG SpriteAnimationLUT SPRITE.brake
  PTRLONG SpriteAnimationLUT SPRITE.dashboard
  PTRLONG SpriteAnimationLUT SPRITE.steering_wheel.normal
  PTRLONG SpriteAnimationLUT SPRITE.steering_wheel.left
  PTRLONG SpriteAnimationLUT SPRITE.steering_wheel.right
  PTRLONG SpriteAnimationLUT SPRITE.super
  PTRLONG SpriteAnimationLUT SPRITE.life_car
  PTRLONG SpriteAnimationLUT SPRITE.life_counter
  PTRLONG SpriteAnimationLUT SPRITE.life_counter
  PTRLONG SpriteAnimationLUT SPRITE.points.normal
  PTRLONG SpriteAnimationLUT SPRITE.points.extra
  PTRLONG SpriteAnimationLUT SPRITE.bang

.ends	

  ;SPRITE_ANIMATION zero
  SPRITE_ANIMATION right_arrow
  SPRITE_ANIMATION left_arrow
  SPRITE_ANIMATION turbo
  SPRITE_ANIMATION brake
  SPRITE_ANIMATION dashboard
  SPRITE_ANIMATION steering_wheel.normal
  SPRITE_ANIMATION steering_wheel.left
  SPRITE_ANIMATION steering_wheel.right
  SPRITE_ANIMATION super
  SPRITE_ANIMATION life_car
  SPRITE_ANIMATION life_counter
  SPRITE_ANIMATION points.normal
  SPRITE_ANIMATION points.extra
  SPRITE_ANIMATION bang
