import re
import sys                               
#import os
import pyperclip 
import logging #For debugging

#Setup Logging
logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] - %(message)s')

if len(sys.argv) < 2: logging.error('USAGE: Assembler.py <sourcefile>'); exit()

lines = []
jmpShortcuts = {}

opCodes = { 'NOP':'0',  'ADD':'1',  'SUB':'2',  'NND':'3',  'CMP':'4',  'JMP':'5',  'JGT':'6',  'JIE':'7',
            'JLT':'8',  'SRV':'9',  'CPR':'10', 'RCL':'11', 'MCL':'12', 'LDM':'13', 'LDR':'14', 'SMV':'15',
            'CLR':'16', 'DWP':'17', 'SRC':'18', 'SGC':'19', 'SBC':'20', 'DWI':'21', 'SVV':'22', 'RVV':'23',
            'CLS':'24', 'WTT':'25', 'CLT':'26', 'GKI':'27', 'RNG':'28', 'HLT':'29', 'RET':'30', 'POP':'31',
            'PUSH':'32', 'SPC':'33', 'RXY':'34'}
keywords = {'REG00':'00', 'REG01':'01', 'REG02':'02', 'REG03':'03', 'REG04':'04', 'REG05':'05', 'REG06':'06', 'REG07':'07',
            'REG08':'08', 'REG09':'09', 'REG0A':'0A', 'REG0B':'0B', 'REG0C':'0C', 'REG0D':'0D', 'REG0E':'0E', 'REG0F':'0F',
            'REG10':'10', 'REG11':'11', 'REG12':'12', 'REG13':'13', 'REG14':'14', 'REG15':'15', 'REG16':'16', 'REG17':'17',
            'REG18':'18', 'REG19':'19', 'REG1A':'1A', 'REG1B':'1B', 'REG1C':'1C', 'REG1D':'1D', 'REG1E':'1E', 'REG1F':'1F',} # ----------------------------------------------------------------------to add the other regs
variables = {}
   
    
linesWithoutShorts = []
newLines = []
    

try: f = open(sys.argv[1], 'r')  # Read file by arguments when starting it
except Exception: logging.error("Can't find file \'" + sys.argv[1] + "\'."); exit(1)

while True:
    line = f.readline()
    
    if not line: break #If the line is empty just skip it while loop
   
    if (line.find(';') != -1): line = line[0:line.find(';')] # delete comments
    line = line.replace('\t', ' ') #Replace tabs with spaces
    line = line.strip() # Remove leading/trailing whitespaces
    line = re.sub(' +', ' ', line)
    
    
    lines.append(line)
f.close()
i = 0 #The current line for jmpShortcuts
for l in lines:
    split = re.split(' ', l)
    
    if not l: continue #if the line is empty skip it
    elif l[0] == '.': jmpShortcuts[l[1:]] = i; continue
    elif split[0][0] == '-': variables[split[0][1:]] = keywords.get(split[1].upper()); continue
    else: linesWithoutShorts.append(l)
    
    i+=1
    #lineItems = re.split(' ,|, |,| |\|', l)
    #lineItems2 = [lineItems[0]]
    #
    #if(lineItems[1] is not in keywords and (lineItems[2] == '==' or lineItems[2] == '=') and lineItems[3].upper() is in keywords) #Here i stopped because i thought that this will be just a loss of time
    ##Change variables with their coresponding register number
    #if lineItems[1][:2].lower() != '0x' and lineItems[1] not in opCodes:
    #    if lineItems[1] in keywords:
    #        lineItems2.append(keywords.get(lineItems[1]))
    #    elif lineItems[1] in variables:
    #        lineItems2.append(variables.get(lineItems[1]))
    #if lineItems[2][:2].lower() != '0x' and lineItems[2] not in opCodes:
    #    if lineItems[2] in keywords:
    #        lineItems2.append(keywords.get(lineItems[2]))
    #    elif lineItems[2] in variables:
    #        lineItems2.append(variables.get(lineItems[2]))
    #linesWithoutShorts.append(l)
print(variables, '\n')
print("-----------------------")
print(jmpShortcuts, '\n')
#print(linesWithoutShorts)
for i, j in enumerate(linesWithoutShorts):
    
    if not j: continue #If the line is empty just skip it
    absoluteLine = lines.index(j) + 1 #Plus one cuz in the editor i see it starting from 1 not from 0
    lineItems = re.split(' ,|, |,| |\|', j) #Split on " ," or ", " or "," or " "
    lineItems2 = []
    
    #Error checking And keyword getting replaced by their values
    try: #Try and catch because you can go out of bounds from the splittedLine array
        if(lineItems[0].upper() not in opCodes): logging.error(f"Wrong usage of operation codes at line {absoluteLine}.")
        if(lineItems[0] == 'WTT'): print(undefined) #A special case(I use print(undefined) so i can leave the try except cuz i couldn't find a better way)
        
        for idx in range(1, 3): #For both lineItems
            if(lineItems[idx].upper() in keywords): lineItems[idx] = '0x' + keywords.get(lineItems[idx].upper())
            elif(lineItems[idx] in jmpShortcuts):   lineItems[idx] = hex(jmpShortcuts.get(lineItems[idx]))
            elif(lineItems[idx] in variables):      lineItems[idx] = variables[lineItems[idx]]
            elif(lineItems[idx][:2] == '0x'): pass #It's in hex already so I skip it
            else: logging.error(f"Parameter {idx} couldn't be recognized at line {absoluteLine}")
    except (OverflowError, IndexError, NameError) as e: pass
    print(lineItems)
    op = lineItems[0]
    #print(op)
    
    if op in opCodes: #Set operation code name
        lineItems2.append(format(int(opCodes[op]), '02X'))
        
        if   op == 'NOP': continue #Nop doesn't count as a line and its just erased
        elif op in ('ADD', 'SUB', 'NND', 'CMP', 'CPR', 'DWP', 'SVV', 'RVV', 'LDR', 'LDM', 'SMV', 'RXY'): #With two registers
            lineItems2.append(format(int(lineItems[1], 16), '02X'))
            lineItems2.append(format(int(lineItems[2], 16), '02X'))
            lineItems2.append('000')
        elif op in ('JMP', 'JGT', 'JIE', 'JLT'):
            lineItems2.append('0000')
            
            lineItems2.append(format(int(lineItems[1], 16), '03X'))
        elif op in ('SRV'): #Special case
            lineItems2.append(format(int(lineItems[1], 16), '02X'))
            lineItems2.append(format(int(lineItems[2], 16), '05X'))
            #lineItems2.append(lineItems[2][2:])
        elif op in ('RCL', 'MCL', 'GKI', 'SRC', 'SGC', 'SBC', 'RNG', 'POP', 'PUSH', 'SPC'): #With one register
            #if lineItems[1][:2] != '0x': #A special case if you want to input the jmpShortcut as a parameter
            #    try:
            #        lineItems[1] = hex(lineItems[1])
            #    except ValueError:
            #        print(logging.error(f"The number on line {absoluteLine} has a wrong prefix that's not '0x' or it isn't an integer"))
            
            lineItems2.append(format(int(lineItems[1], 16), '02X'))
            lineItems2.append('00000')
        elif op in ('CLR', 'DWI', 'CLS', 'CLT', 'HLT', 'RET'): lineItems2.append('0000000')#Without any arguments
        elif op == 'WTT': #Only Write To Terminal | Special case reg0 + reg1 for 7 bit ASC
            if lineItems[1] == "<space>": lineItems2.append("20")
            elif lineItems[1] == "<back>" or lineItems[1] == "<backspace>": lineItems2.append("08")
            else: lineItems2.append(str(hex(ord(lineItems[1]))[2:]))
            lineItems2.append('00000')
    else: logging.error(f"Invalid operation code at line {absoluteLine}")
    #print(lineItems2)
    if len(''.join(lineItems2)) != 9: logging.error(f"The length of the line {absoluteLine} compiled is {len(''.join(lineItems2))} digits. Possible bug in code or a mistake by the creator of the assembly file. Take a look at it!") #Check length of line
    
    newLines.append(''.join(lineItems2))
joinedLines = ' '.join(newLines)
print(joinedLines) #Print without parentheses and commas

pyperclip.copy(joinedLines)
print("\nInstructions copied!")