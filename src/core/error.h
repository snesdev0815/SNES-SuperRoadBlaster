.include "src/config/config.inc"


;defines
.define errStrt	10

.enum errStrt export
E_ObjLstFull	db
E_ObjRamFull	db
E_StackTrash	db
E_Brk					db
E_StackOver		db
E_Sa1IramCode			db	;unable to copy stuff to sa1 iram buffer(needs to be write-enabled)
E_Sa1IramClear	db
E_Sa1Test db
E_Sa1NoIrq db
E_Todo db
E_SpcTimeout db
E_ObjBadHash	db
E_ObjBadMethod db
E_BadScript db
E_StackUnder db
E_Cop db
E_ScriptStackTrash db
E_UnhandledIrq	db
E_Sa1BWramClear db
E_Sa1NoBWram db
E_Sa1BWramToSmall db
E_Sa1DoubleIrq	db
E_SpcNoStimulusCallback	db
E_Msu1NotPresent db
E_Msu1FileNotPresent db
E_Msu1SeekTimeout db
E_Msu1InvalidFrameRequested db
E_DmaQueueFull db
E_InvalidDmaTransferType db
E_InvalidDmaTransferLength db
E_VallocBadStepsize db
E_VallocEmptyDeallocation db
E_UnitTestComplete db
E_UnitTestFail db
E_VallocInvalidLength db
E_CGallocInvalidLength db
E_CGallocBadStepsize db
E_CGallocInvalidStart db
E_CGallocEmptyDeallocation db
E_ObjNotFound db
E_BadParameters db
E_OutOfVram db
E_OutOfCgram db
E_InvalidException db
E_Msu1InvalidFrameCycle db
E_Msu1InvalidChapterRequested db
E_Msu1InvalidChapter db
E_Msu1AudioSeekTimeout db
E_Msu1AudioPlayError db
E_ObjStackCorrupted db
E_BadEventResult db
E_abstractClass db
E_NoChapterFound db
E_NoCheckpointFound db
E_BadSpriteAnimation db
E_AllocatedVramExceeded db
E_AllocatedCgramExceeded db
E_InvalidDmaChannel db
E_DmaChannelEmpty db
E_NoDmaChannel db
E_VideoMode db
E_BadBgAnimation db
E_BadBgLayer db
E_NtscUnsupported db
E_WallocBadStepsize db
E_WallocEmptyDeallocation db
E_OutOfWram db
E_BadInputDevice db
E_ScoreTest db
E_Msu1FrameBad db
E_BadIrq db
E_NoIrqCallback db
E_BadIrqCallback db
E_SramBad db
E_MaxException ds 0
.ende

;data structures

;ram buffers
.base RAM
;this is where exception handler stores temp vars for exception display
.ramsection "exception cpu status buffr" bank 0 slot 2
excStack	dw
excA	dw
excY	dw
excX	dw
excDp	dw
excDb	db
excPb	db
excFlags	db
excPc	dw
excErr	dw
excArgs	ds 8
.ends


;data includes
.base BSL
.section "exception font tiles" superfree
	FILEINC ExcFontTiles "build/data/font/fixed8x8.gfx_font.tiles"
.ends

.section "exception font pal" superfree
	FILEINC ExcFontPal "build/data/font/fixed8x8.gfx_font.palette" 8
.ends
/*
.section "exception string command lut"
	ExcStrCmdLut:
		PTRNORM ExcStrCmdLut SUB_TC_end
		PTRNORM ExcStrCmdLut SUB_TC_sub
		PTRNORM ExcStrCmdLut SUB_TC_iSub
		PTRNORM ExcStrCmdLut SUB_TC_dSub
		PTRNORM ExcStrCmdLut SUB_TC_diSub
		PTRNORM ExcStrCmdLut SUB_TC_pos
		PTRNORM ExcStrCmdLut SUB_TC_brk
		PTRNORM ExcStrCmdLut SUB_TC_hToS
.ends
*/

.section "err-msg string LUT" superfree
	ExcErrMsgStrLut:
		.db T_EXCP_E_ObjLstFull.PTR
		.db T_EXCP_E_ObjRamFull.PTR
		.db T_EXCP_E_StackTrash.PTR
		.db T_EXCP_E_Brk.PTR
		.db T_EXCP_E_StackOver.PTR
		.db T_EXCP_E_Sa1IramCode.PTR
		.db T_EXCP_E_Sa1IramClear.PTR
		.db T_EXCP_Sa1Test.PTR
		.db T_EXCP_Sa1NoIrq.PTR
		.db T_EXCP_Todo.PTR
		.db T_EXCP_SpcTimeout.PTR
		.db T_EXCP_ObjBadHash.PTR
		.db T_EXCP_ObjBadMethod.PTR
		.db T_EXCP_BadScript.PTR
		.db T_EXCP_StackUnder.PTR
		.db T_EXCP_E_Cop.PTR
		.db T_EXCP_E_ScriptStackTrash.PTR
		.db T_EXCP_E_UnhandledIrq.PTR
		.db T_EXCP_E_Sa1BWramClear.PTR
		.db T_EXCP_E_Sa1NoBWram.PTR
		.db T_EXCP_E_Sa1BWramToSmall.PTR
		.db T_EXCP_E_Sa1DoubleIrq.PTR
		.db T_EXCP_E_SpcNoStimulusCallback.PTR
		.db T_EXCP_E_Msu1NotPresent.PTR
		.db T_EXCP_E_Msu1FileNotPresent.PTR
		.db T_EXCP_E_Msu1SeekTimeout.PTR
		.db T_EXCP_E_Msu1InvalidFrameRequested.PTR
		.db T_EXCP_E_DmaQueueFull.PTR
		.db T_EXCP_E_InvalidDmaTransferType.PTR
		.db T_EXCP_E_InvalidDmaTransferLength.PTR		
		.db T_EXCP_E_VallocBadStepsize.PTR
		.db T_EXCP_E_VallocEmptyDeallocation.PTR
		.db T_EXCP_E_UnitTestComplete.PTR
		.db T_EXCP_E_UnitTestFail.PTR
		.db T_EXCP_E_VallocInvalidLength.PTR
		.db T_EXCP_E_CGallocInvalidLength.PTR
		.db T_EXCP_E_CGallocBadStepsize.PTR
		.db T_EXCP_E_CGallocInvalidStart.PTR
		.db T_EXCP_E_CGallocEmptyDeallocation.PTR
		.db T_EXCP_E_ObjNotFound.PTR
		.db T_EXCP_E_BadParameters.PTR
		.db T_EXCP_E_OutOfVram.PTR
		.db T_EXCP_E_OutOfCgram.PTR
		.db T_EXCP_E_InvalidException.PTR
		.db T_EXCP_E_Msu1InvalidFrameCycle.PTR
		.db T_EXCP_E_Msu1InvalidChapterRequested.PTR
		.db T_EXCP_E_Msu1InvalidChapter.PTR
		.db T_EXCP_E_Msu1AudioSeekTimeout.PTR
		.db T_EXCP_E_Msu1AudioPlayError.PTR
		.db T_EXCP_E_ObjStackCorrupted.PTR
		.db T_EXCP_E_BadEventResult.PTR
		.db T_EXCP_E_abstractClass.PTR
		.db T_EXCP_E_NoChapterFound.PTR
		.db T_EXCP_E_NoCheckpointFound.PTR
		.db T_EXCP_E_BadSpriteAnimation.PTR
		.db T_EXCP_E_AllocatedVramExceeded.PTR
		.db T_EXCP_E_AllocatedCgramExceeded.PTR
		.db T_EXCP_E_InvalidDmaChannel.PTR
		.db T_EXCP_E_DmaChannelEmpty.PTR
		.db T_EXCP_E_NoDmaChannel.PTR
		.db T_EXCP_E_VideoMode.PTR
		.db T_EXCP_E_BadBgAnimation.PTR
		.db T_EXCP_E_BadBgLayer.PTR
		.db T_EXCP_E_NtscUnsupported.PTR
		.db T_EXCP_E_WallocBadStepsize.PTR
		.db T_EXCP_E_WallocEmptyDeallocation.PTR
		.db T_EXCP_E_OutOfWram.PTR
		.db T_EXCP_E_BadInputDevice.PTR
		.db T_EXCP_E_ScoreTest.PTR
		.db T_EXCP_E_Msu1FrameBad.PTR
        .db T_EXCP_E_BadIrq.PTR
        .db T_EXCP_E_NoIrqCallback.PTR
        .db T_EXCP_E_BadIrqCallback.PTR
        .db T_EXCP_E_SramBad.PTR

.ends

