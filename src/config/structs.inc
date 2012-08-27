;global structs

.struct oopObjHash
id			db	;class id
count		db	;createobj call count
pntr		dw	;relative pointer to obj in obj stack
.endst


;sa1 structs
.STRUCT vertex
x	db
y	db
.ENDST

.STRUCT edge
leE	db
riE	db
.ENDST

.STRUCT tile
p ds 64
.ENDST

.STRUCT linBuff
strt dw
end  dw
dpag dw
.ENDST

.STRUCT linDpag
lin dw
.ENDST


.STRUCT lineDist
dx db
dy db
startx db
starty db
endx db
endy db
march db	;x=0,y=$80
dir	db	;left=0,right=$80
countr	db	;division step counter
posx	db
posy	db
void	db
.ENDST

;spc structures
.STRUCT callbackBuff
pointer		dw	;pointer to callback routine. $ffff means empty
.ENDST

;iterator structs

.struct iteratorStruct
  self ds 4
  properties dw
  target ds 4
  index dw
  count dw
  sort.count dw
  sort.target dw
  sort.key dw
  sort.first ds 4
  sort.second ds 4
.endst

;sprite/dimensions structs

.struct dimensionStruct
  position.x ds 3
  position.y ds 3
  position.z ds 3
  size.x dw
  size.y dw
.endst

.struct eventStruct
  chapterId dw
  startFrame dw
  endFrame dw
  result dw
  resultTarget dw
  msu1Handler ds 4
  player ds 4
.endst

.struct scriptStruct
  timestamp.start dw
  initAdress dw
.endst

.struct animationStruct
  id db
  pointer ds 3
  buffer.x db
  buffer.y db
  buffer.tile db
  buffer.flags db
  buffer.nametable db
  displacement.x dw
  displacement.y dw

  isPlaying db
  isLooping db
  isColorMath db
  priority db
  speed db

  frame.current dw
  frame.last dw
  frame.max dw
  frame.pointer ds 3
  frame.tiles.length dw
  frame.tilemap.length dw
  frame.palette.length dw

  tiles.id db
  tiles.start dw
  tiles.length dw
  tiles.startid db
  tiles.bpp db

  palette.id db
  palette.start dw
  palette.length dw
  palette.startid db

  tilemap.id db
  tilemap.start dw
  tilemap.length dw
  tilemap.startid db

  ramBuffer.id db
  ramBuffer.start dw
  ramBuffer.length dw

.endst

.struct hdmaStruct
  channel db	;msb set if allocated
  isActive db
  target db
  indirect.bank db
  flags db	;directly correspond to dmap0-flags
  table.adress ds 3
  ramBuffer.start dw
  ramBuffer.length dw
  ramBuffer.id db
.endst

.struct static.string.struct
  current.pointer ds 3	;tmp - tmp+2
  screen.position dw	;tmp+4,tmp+5
  screen.line dw	;tmp+4,tmp+5
  screen.margin.left dw	;tmp+6, tmp+7
  substring.length dw	;tmp+8, tmp+9
  substring.pointer ds 3	;tmp+10 - tmp+12
  current.stack	dw 	;tmp+13 - tmp+14
  substring.buffer ds 4	;tmp+15 - tmp+18  
.endst

.struct paletteStruct
  color.start dw
  color.length dw

  ramBuffer.id db
  ramBuffer.start dw
  ramBuffer.length dw

.endst
