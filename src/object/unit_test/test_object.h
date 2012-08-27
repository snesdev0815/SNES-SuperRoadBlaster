.include "src/config/config.inc"


;zp-vars
.enum 0
  iterator INSTANCEOF iteratorStruct
  _tmp ds 8
  zpLen ds 0
.ende

;object class static flags, default properties and zero page 
.define CLASS.FLAGS OBJECT.FLAGS.Present
.define CLASS.PROPERTIES OBJECT.PROPERTIES.isUnitTest
.define CLASS.ZP_LENGTH zpLen

.base BSL
.bank 0 slot 0
/*.section "unit_test_obj"
	OOPOBJ Test_object $81 zpLen testParameterReturn
.ends*/



