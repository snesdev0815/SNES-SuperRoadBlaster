.include "src/config/config.inc"


;ram buffers

;data includes
.base BSL
.section "textstring lut" superfree
TextstringLUT:
	PTRLONG TextstringLUT T_EXCP_exception
	PTRLONG TextstringLUT T_EXCP_starLine
	PTRLONG TextstringLUT T_EXCP_E_ObjLstFull
	PTRLONG TextstringLUT T_EXCP_E_ObjRamFull
	PTRLONG TextstringLUT T_EXCP_E_StackTrash
	PTRLONG TextstringLUT T_EXCP_E_Brk
	PTRLONG TextstringLUT T_EXCP_E_StackOver
	PTRLONG TextstringLUT T_EXCP_LastCalled
	PTRLONG TextstringLUT T_EXCP_ClassMethod
	PTRLONG TextstringLUT T_EXCP_HexTest
	PTRLONG TextstringLUT T_EXCP_E_Sa1IramCode
	PTRLONG TextstringLUT T_EXCP_E_Sa1IramClear
	PTRLONG TextstringLUT T_EXCP_Sa1Test
	PTRLONG TextstringLUT T_EXCP_cpuInfo
	PTRLONG TextstringLUT T_EXCP_sa1Info
	PTRLONG TextstringLUT T_EXCP_irqInfo
	PTRLONG TextstringLUT T_EXCP_Sa1NoIrq
	PTRLONG TextstringLUT T_EXCP_Todo
	PTRLONG TextstringLUT T_EXCP_SpcTimeout
	PTRLONG TextstringLUT T_EXCP_ObjBadHash
	PTRLONG TextstringLUT T_EXCP_ObjBadMethod
	PTRLONG TextstringLUT T_EXCP_undefined
	PTRLONG TextstringLUT T_EXCP_BadScript
	PTRLONG TextstringLUT T_EXCP_StackUnder
	PTRLONG TextstringLUT T_EXCP_E_Cop
	PTRLONG TextstringLUT T_EXCP_E_ScriptStackTrash
	PTRLONG TextstringLUT T_EXCP_E_UnhandledIrq
	PTRLONG TextstringLUT T_EXCP_E_Sa1BWramClear
	PTRLONG TextstringLUT T_EXCP_E_Sa1NoBWram
	PTRLONG TextstringLUT T_EXCP_E_Sa1BWramToSmall
	PTRLONG TextstringLUT T_EXCP_E_Sa1DoubleIrq
	PTRLONG TextstringLUT T_EXCP_Sa1BwramReq
	PTRLONG TextstringLUT T_EXCP_E_SpcNoStimulusCallback
	PTRLONG TextstringLUT T_EXCP_E_Msu1NotPresent
	PTRLONG TextstringLUT T_EXCP_E_Msu1FileNotPresent
	PTRLONG TextstringLUT T_EXCP_E_Msu1SeekTimeout
	PTRLONG TextstringLUT T_EXCP_E_Msu1InvalidFrameRequested
	PTRLONG TextstringLUT T_EXCP_E_DmaQueueFull
	PTRLONG TextstringLUT T_EXCP_E_methodStackObj
	PTRLONG TextstringLUT T_EXCP_E_InvalidDmaTransferType
	PTRLONG TextstringLUT T_EXCP_E_InvalidDmaTransferLength
	PTRLONG TextstringLUT T_EXCP_E_VallocBadStepsize
	PTRLONG TextstringLUT T_EXCP_E_VallocEmptyDeallocation
	PTRLONG TextstringLUT T_EXCP_E_UnitTestComplete
	PTRLONG TextstringLUT T_EXCP_E_UnitTestFail
	PTRLONG TextstringLUT T_EXCP_E_VallocInvalidLength
	PTRLONG TextstringLUT T_EXCP_E_CGallocInvalidLength
	PTRLONG TextstringLUT T_EXCP_E_CGallocBadStepsize
	PTRLONG TextstringLUT T_EXCP_E_CGallocInvalidStart
	PTRLONG TextstringLUT T_EXCP_E_CGallocEmptyDeallocation
	PTRLONG TextstringLUT T_EXCP_E_ObjNotFound
	PTRLONG TextstringLUT T_EXCP_E_BadParameters
	PTRLONG TextstringLUT T_EXCP_E_OutOfVram
	PTRLONG TextstringLUT T_EXCP_E_OutOfCgram
	PTRLONG TextstringLUT T_EXCP_E_InvalidException
	PTRLONG TextstringLUT T_EXCP_E_Msu1InvalidFrameCycle
	PTRLONG TextstringLUT T_EXCP_E_Msu1InvalidChapterRequested
	PTRLONG TextstringLUT T_EXCP_E_Msu1InvalidChapter
	PTRLONG TextstringLUT T_EXCP_E_Msu1AudioSeekTimeout
	PTRLONG TextstringLUT T_EXCP_E_Msu1AudioPlayError
	PTRLONG TextstringLUT T_EXCP_E_ObjStackCorrupted
	PTRLONG TextstringLUT T_EXCP_E_BadEventResult
	PTRLONG TextstringLUT T_EXCP_E_abstractClass
	PTRLONG TextstringLUT T_EXCP_E_NoChapterFound
	PTRLONG TextstringLUT T_EXCP_E_NoCheckpointFound
	PTRLONG TextstringLUT T_EXCP_E_BadSpriteAnimation
	PTRLONG TextstringLUT T_EXCP_E_AllocatedVramExceeded
	PTRLONG TextstringLUT T_EXCP_E_AllocatedCgramExceeded
	PTRLONG TextstringLUT T_EXCP_E_InvalidDmaChannel
	PTRLONG TextstringLUT T_EXCP_E_DmaChannelEmpty
	PTRLONG TextstringLUT T_EXCP_E_NoDmaChannel
	PTRLONG TextstringLUT T_EXCP_E_VideoMode
	PTRLONG TextstringLUT T_EXCP_E_BadBgAnimation
	PTRLONG TextstringLUT T_EXCP_E_BadBgLayer
	PTRLONG TextstringLUT T_EXCP_E_NtscUnsupported
	PTRLONG TextstringLUT T_EXCP_E_WallocBadStepsize
	PTRLONG TextstringLUT T_EXCP_E_WallocEmptyDeallocation
	PTRLONG TextstringLUT T_EXCP_E_OutOfWram
	PTRLONG TextstringLUT T_EXCP_E_BadInputDevice
	PTRLONG TextstringLUT T_EXCP_E_ScoreTest
    PTRLONG TextstringLUT T_EXCP_E_Msu1FrameBad
	PTRLONG TextstringLUT T_hallOfFame
	PTRLONG TextstringLUT T_highScore
	PTRLONG TextstringLUT T_title
	PTRLONG TextstringLUT T_schleck
	PTRLONG TextstringLUT T_scoreEntry
	PTRLONG TextstringLUT T_scoreEntryName
    PTRLONG TextstringLUT T_EXCP_E_BadIrq
    PTRLONG TextstringLUT T_EXCP_E_NoIrqCallback
    PTRLONG TextstringLUT T_EXCP_E_BadIrqCallback
    PTRLONG TextstringLUT T_levelComplete
    PTRLONG TextstringLUT T_EXCP_E_SramBad
	PTRLONG TextstringLUT T_max
	
.ends

