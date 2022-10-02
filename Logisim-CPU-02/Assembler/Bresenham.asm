;Reset registers
RCL 0x0 ;incX
RCL 0x1 ;dX
RCL 0x2 ;incY
RCL 0x3 ;dY
RCL 0x4 ;XaY
RCL 0x5 ;cmpt
RCL 0x6 ;incD
RCL 0x7 ;incS
RCL 0x8 ;err
RCL 0x9 ;X
RCL 0xA ;Y
RCL 0xB ;B.x
RCL 0xC ;B.y
RCL 0xD ;Temp Reg
RCL 0xE ;Temp Reg 2
;Secondary RAM
;A.x
;A.y
;B.x
;B.y

;Load all values
LDM 0x0, 0x9;X = A.x
LDM 0x1, 0xA;Y = A.y
LDM 0x2, 0xB;B.x
LDM 0x3, 0xC;B.y

SPC 00000, 111111, 11111 

;incX = sgn(B.x-A.x)
CPR 0x0, 0xB
SUB 0x0, 0x9

SRV 0xD, 000
CMP 0x0, 0xD
JIE endOfIf01 ;If less than
JGT endOfIf01
	SRV 0x0, 0xFFF
	JMP endOfSGN1
endOfIf01:
JIE endOfIf02 ;If Greater Than
JLT endOfIf02
	SRV 0x0, 0x001
	JMP endOfSGN1
endOfIf02:
endOfSGN1:

;dX = abs(B.x-A.x)
CPR 0x1, 0xB
SUB 0x1, 0x9

CMP 0x1, 0xD
JIE endOfABS1 ;If less than
JGT endOfABS1
	SRV 0xD, 0x001 ;Turn for example 'FFFF' in '0001' using 2's compliment
	SUB 0x1, 0xD
	NND 0x1, 0x1
endOfABS1:

;incY = sgn(B.y-A.y)
CPR 0x2, 0xC
SUB 0x2, 0xA

SRV 0xD, 000
CMP 0x2, 0xD
JIE endOfIf03 ;If less than
JGT endOfIf03
	SRV 0x2, 0xFFF
	JMP endOfSGN2
endOfIf03:
JIE endOfIf04 ;If Greater Than
JLT endOfIf04
	SRV 0x2, 0x001
	JMP endOfSGN2
endOfIf04:
endOfSGN2:

;dY = abs(B.y-A.y)
CPR 0x3, 0xC
SUB 0x3, 0xA

SRV 0xD, 000 ;Send because the previously used ABS func made it 001
CMP 0x3, 0xD
JIE endOfABS2 ;If less than
JGT endOfABS2
	SRV 0xD, 0x001 ;Turn for example 'FFFF' in '0001' using 2's compliment
	SUB 0x3, 0xD
	NND 0x3, 0x3
endOfABS2:

;XaY = dX > dY
CMP 0x1, 0x3

JGT endOfIf05 ;If less than or Equal
	SRV 0x4, 0x000 ;Return false
	JMP endOfBool1
endOfIf05:
JIE endOfIf06 ;If Greater Than
JLT endOfIf06
	SRV 0x4, 0x001 ;Return true
	JMP endOfBool1
endOfIf06:
endOfBool1:

;cmpt = max(dX, dY)
;CMP 0x1, 0x3 was previously used so no need now
JIE	endOfIf07 ;If Greater than
JLT endOfIf07
	CPR 0x5, 0x1 ;Return dX to cmpt
endOfIf07:
JGT endOfIf08 ;If dX is less than or equal just return dY
	CPR 0x5, 0x3
endOfIf08:

;incD = -2 * abs(dX - dY)
CPR 0x6, 0x1 ;Make incD dX - dY
SUB 0x6, 0x3

SRV 0xD, 0x000 ;Start of kinda inverted abs function for incD ;HERE ERROR CAN HAPPEN
CMP 0x6, 0xD
JLT endOfIf09 ;If dX - dY is bigger than 0 then multiply it by -1 by using 2's compliment and than multiply by 2
JIE endOfIf09
	SRV 0xD, 0x001
	SUB 0x6, 0xD
	NND 0x6, 0x6
	ADD 0x6, 0x6 ;Multiply by 2
endOfIf09:

;incS = 2 * min(dX, dY)
CMP 0x1, 0x3

JIE	endOfIf0A ;If Less than
JGT endOfIf0A
	CPR 0x7, 0x1 ;Return dX to incS
endOfIf0A:
JLT endOfIf0B ;If dX is Greater than or equal just return dY
	CPR 0x7, 0x3
endOfIf0B:

ADD 0x7, 0x7 ;Multiply by 2

;err = incD + cmpt
CPR 0x8, 0x6
ADD 0x8, 0x5

;while cmpt >= 0
SRV 0xD, 0x000
whileStart1:
CMP 0x5, 0xD ;If cmpt is bigger than or equal to zero
JLT whileEnd1
	DWP 0x9, 0xA
	
	SRV 0xE, 0x001 ;cmpt--
	SUB 0x5, 0xE
	
	
	
	
	
	
	
	
	
	;#####GIVEEE A TEST TO THIS NEW CODE I THINK IT"S WRONG BECAUSE OF THE ADD 0x8, 0x7
	;############ALSO I THINK ITS NOT ONLY THE ADD THAT IS KINDA WRONG I SHOULD MAKE THIS PART LIKE ITS INTENDET TO BE NOT TO SHORTEN IT like tHAT
	
	
	;CMP 0x8, 0xD;Start of kinda messed up if statements..... But they work if you give them a try, I hope!
	;JLT endOfMess1
	;	JMP endOfMess2
	;endOfMess1:
	;CMP 0x4, 0xD
	;JIE endOfMess3
	;	endOfMess2:
	;	ADD 0x9, 0x0
	;endOfMess3:
	;CMP 0x8, 0xD
	;JLT endOfMess4
	;	JMP endOfMess5
	;endOfMess4:
	;CMP 0x4, 0xD
	;JGT endOfMess6
	;JLT endOfMess6	
	;	endOfMess5:
	;	ADD 0xA, 0x2
	;endOfMess6:
	;CMP 0x8, 0xD
	;JLT endOfMess7
	;	ADD 0x8, 0x6
	;	JMP endOfMess8
	;endOfMess7:
	;ADD 0x8, 0x7 <--------------------HERE
	;endOfMess8:
	
	
	CMP 0x8, 0xD
	JLT endOfIf0C;If Greater than or equal
		JMP mess0
	endOfIf0C:
	CMP 0x4, 0xD
	JIE endOfIf0D;If XaY is not 0
		mess0:
		ADD 0x9, 0x0
	endOfIf0D:
	
	CMP 0x8, 0xD
	JLT endOfIf0E ;If Geater than or equal
		JMP mess1
	endOfIf0E:
	CMP 0x4, 0xD
	JGT endOfIf0F
	JLT endOfIf0F
		mess1:
		ADD 0xA, 0x2
	endOfIf0F:
	
	CMP 0x8, 0xD
	JLT endOfIf10;If Greater than or equal
		ADD 0x8, 0x6
		JMP endOfIf11 ;Needed for else
	endOfIf10: ;Else
	ADD 0x8, 0x7
	endOfIf11:
	
	JMP whileStart1 ;Jump to the start because there is a check for cmpt
	;CMP 0x5, 0xD
	;JGT whileStart1
	;JIE whileStart1
whileEnd1:
HLT