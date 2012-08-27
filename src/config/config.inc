
.MEMORYMAP
DEFAULTSLOT 0
SLOTSIZE $10000
SLOT 0 $0000	;rom

SLOTSIZE $10000-$2000
SLOT 1 $7e2000	;ram in bank $7e

SLOTSIZE $2000
SLOT 2 16	;zero-page ram. 16=debug value to check if all routines relocate properly
.ENDME

.ROMBANKSIZE $10000    ; Every ROM bank is 64 KBytes in size, also necessary.
.ROMBANKS 4           ; 2Mbits -- Tells WLA that you want to use 32 ROM banks.


/*
wla dx is a fucking piece of crap.
it's not even able to properly allocate memory required for below features, resulting in unrelated data spilling into the header.
what a fucking disgrace.
.snesheader
name "SUPER ROAD BLASTER   "
hirom
fastrom
cartridgetype $0
romsize 10
sramsize 0
country 0
licenseecode $33
version 0
.endsnes


.SNESNATIVEVECTOR
COP    StopCop
BRK    Stop
ABORT  EmptyHandler
NMI    NmiHandler
UNUSED IrqHookUp
IRQ    EmptyHandler
.ENDNATIVEVECTOR

.SNESEMUVECTOR
COP    StopCop
ABORT  EmptyHandler
NMI    EmptyHandler
RESET  Boot
IRQBRK EmptyHandler
.ENDEMUVECTOR
*/
.EMPTYFILL 0


;kernel defines:
;bank defines
.def BSL		$c0
.def ROM		$c0
.def RAM		$7e
.def RAM2		RAM+1
.def REGS		$00

.def BANK0_LOROM		$8000

;header defines
.def SNESHEADER.TITLE $ffc0


.include "src/config/globals.inc"

