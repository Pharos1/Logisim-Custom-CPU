;;Snake game in custom asm
-bgColor reg00
-snakeColor reg01
-appleColor reg02
SRV bgColor, 0xFFFF
SRV snakeColor, 0x3E0
SRV appleColor, 0x7C00

-curKey reg03
-one reg09
-curKeyCheck reg0a



SRV curKey, 0x77 ;Make sure it's set to something(in this case 'w')
RCL one



-exitKey reg04
SRV exitKey, 0x65

-maxHeight reg05
-maxWidth reg06

SRV maxHeight, 0x1f
SRV maxWidth, 0x0f

-xOfBG reg07
-yOfBG reg08

RCL xOfBG
RCL yOfBG




-snakeCurX reg0b
-snakeCurY reg0c
RNG snakeCurX
RNG snakeCurY
RCL snakePosInRAM
SRV one, 0x1

LDR snakeCurX, snakePosInRAM ;X
ADD snakePosInRAM, one		;

		
LDR snakeCurY, snakePosInRAM ;Y
ADD snakePosInRAM, one		;

-snakePosInRAM reg0d
;RCL snakePosInRAM

-gameCounter reg0e
RCL gameCounter

-temp0 reg0f
-temp1 reg10

-snakeTempX reg11
-snakeTempY reg15

-snakeArrayLen reg12 	  ;the size of this array(the area that it will take in the secRam)
SRV snakeArrayLen, 0x200 ;height * width = 512(0x200 in hex)

-snakeLength reg13
SRV snakeLength, 0x1

-applePosX reg14
-applePosY reg15
RCL applePosX
RCL applePosY

-isAppleSpawned reg16 ;0x1 is true and 0x0 is false
RCL isAppleSpawned

;Background
.background	
	SPC bgColor
	SRV one, 0x1
	.loopYStart
		.loopXStart
			DWP xOfBG, yOfBG
			
			ADD xOfBG, one
			
			CMP xOfBG, maxWidth
			
			JLT loopXStart
			JIE loopXStart
		ADD yOfBG, one
		
		SUB xOfBG, maxHeight ;xOfBG - Maxheight - 1 cuz it had to be 40 to leave the xLoop
		SUB xOfBG, one     ;
		
		CMP yOfBG, maxHeight
		JLT loopYStart
		JIE loopYStart
		
.gameLoop
	SRV temp0, 0x0
	
	GKI curKeyCheck ;Start of checking if key is 0 and if it is it, shouldn't change the curKey
	CMP temp0, curKeyCheck
	JIE endOfCheckKey
	CPR curKey, curKeyCheck ;Copy it over so it doesn't consume 2 characters everytime
	
	CMP curKey, exitKey  ;If key = exitKey: exit
	JIE endOfGameLoop;
	
	.endOfCheckKey
	
	; Core of the game
	;Apple check
	
	;Snake Movement	
	.snakeMovement
		;If input add or subtract
			;w Check
			SRV temp0, 0x77
			
			CMP curKey, temp0
			JLT endOfWKeyCheck
			JGT endOfWKeyCheck
			
			ADD snakeCurY, one
			
			.endOfWKeyCheck
			
			;a Check
			SRV temp0, 0x61
			
			CMP curKey, temp0
			JLT endOfAKeyCheck
			JGT endOfAKeyCheck
			
			SUB snakeCurX, one
			.endOfAKeyCheck
			
			;s Check
			SRV temp0, 0x73
			
			CMP curKey, temp0
			JLT endOfSKeyCheck
			JGT endOfSKeyCheck
			
			SUB snakeCurY, one
			.endOfSKeyCheck
			
			;d Check
			SRV temp0, 0x64
			
			CMP curKey, temp0
			JLT endOfDKeyCheck
			JGT endOfDKeyCheck
			
			ADD snakeCurX, one
			.endOfDKeyCheck
			
			
			
			;APPLE CHECK
			.appleCheck
				.appleGen
					CMP isAppleSpawned, one
					JIE isAppleEaten
					
					ADD isAppleSpawned, one ;MAke it true
					
					RNG applePosX
					RNG applePosY
					CPR temp0, applePosX
					RXY temp0, applePosY ;Check was it spawned in the snake
					CMP temp0, snakeColor;
					JIE appleGen		 ;
					SPC appleColor 		 ;
					DWP applePosX, applePosY ;If not, spawn it
			
				.isAppleEaten
					CPR temp0, snakeCurX
					RXY temp0, snakeCurY
					
					CMP temp0, appleColor
					JLT endOfIsAppleEaten
					JGT	endOfIsAppleEaten
					
					ADD snakeLength, one
					SUB isAppleSpawned, one ;Make it false
					.endOfIsAppleEaten
					
		SPC snakeColor
		DWP snakeCurX, snakeCurY
	
	.posToSecRam
		LDR snakeCurX, snakePosInRAM ;X
		ADD snakePosInRAM, one		;
		
				
		LDR snakeCurY, snakePosInRAM ;Y
		ADD snakePosInRAM, one		;
	
		CMP snakePosInRAM, snakeArrayLen ;Snake pos can either be 200 or 198 if its greater than or equal to 200 then just subtract 200 to leave it at 0
		JLT endOfPosToSecRam
		
		SUB snakePosInRAM, snakeArrayLen
	.endOfPosToSecRam
	
		
	.removeTheTail
		CPR temp0, snakePosInRAM
		SUB temp0, one ;Remove 2 cuz the new head is ignored in the snakeLength
		SUB temp0, one ;
		
		CPR temp1, snakeLength
		ADD temp1, snakeLength
		;ADD temp1, one ;ADD cuz snakePosInRam is 
		
		;if we have just capped it then it should be zero and we check if its greater than the snakeLength and if thats the case then just add 200 and sub the snakeLength*2(as there is x and y in the ram) to get the tail
		CMP temp0, temp1        ;if less than or equal ADD temp0, snakeArrayLen
		JGT endOfRemoveTailPart
		JIE endOfRemoveTailPart
		
		ADD temp0, snakeArrayLen
		
		.endOfRemoveTailPart
		
		SUB temp0, temp1 ;X
		
		CPR temp1, temp0 ;Y
		ADD temp1, one
		
		CPR snakeTempX, temp0
		CPR snakeTempY, temp1
		
		LDM temp0, temp0 ;Put the value on the place of the address
		LDM temp1, temp1 ;Put the value on the place of the address
		MCL snakeTempX
		MCL snakeTempY
	
	SPC bgColor
	DWP temp0, temp1;Fill it in the bg color
		
	;###############################################HAVE TO MAKE THE APPLE SYSTEM
	;RNG appleToBePlaced; if RVV appleToBePlaced != snakeColor: drawApple else: repeat until done
	;;;;IN THE CODE FOR THE SNAKE MOVEMENT I SHOULD CHECK IF THE NEXT HEAD WILL BE DRAWN OVER THE APPLE AND IF SO, INCREMENT THE LENGTH AND DON'T REMOVE THE TAIL NEXT TIME
	
	
	
	
	ADD gameCounter, one
	DWI ;Output the final image
	
	
	JMP gameLoop
.endOfGameLoop
HLT 