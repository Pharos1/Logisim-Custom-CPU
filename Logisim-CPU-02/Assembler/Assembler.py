import re
import sys                               
import os                               
if len(sys.argv) < 2: print('USAGE: Assembler.py <sourcefile>'); exit(1)

lines = []
jmpShortcuts = {}

#print(hex(int("00000", 2)))
#print(format(int("0000000000011111", 2), '04X'))
#opCodes = { 'NOP':'0',  'ADD':'1',  'SUB':'2',  'NND':'3',  'CMP':'4',  'JMP':'5',  'JGT':'6',  'JIE':'7',
#            'JLT':'8',  'SRV':'9',  'CPR':'10', 'RCL':'11', 'MCL':'12', 'LDM':'13', 'LDR':'14', 'SMV':'15',
#            'SPC':'16', 'DWP':'17', 'HLT':'18'}
            
try: f = open(sys.argv[1], 'r')                     # Read file by arguments when starting it
except: print("ERROR: Can't find file \'" + sys.argv[1] + "\'."); exit(1)

while True:
    line = f.readline()
   
    if not line: break
    
    if (line.find(';') != -1): line = line[0:line.find(';')] # delete comments
    line = line.replace('\t', ' ') #Replace tabs with spaces
    line = line.strip() # Remove leading/trailing whitespaces
    #print(line)
    #line = re.sub(r"[\n\t]*", "", line)
    
    #if '\t' in line: print(f"ERROR AT LINE WITH CONTENTS \'{line}\': Tab was found! Use whitespace instead"); exit()#Error check for tabs
    
    if len(line) > 2 or ':' in line: lines.append(line) # store the line only if it is longer than 2 digits or there are curly braces(because it deletes them)
f.close()
#for i in range(len(lines)): 
#    if (lines[i].find(';') != -1): lines[i] = lines[i][0:lines[i].find(';')]    # delete comments
#TODO: ADD FUNCTIONS like PRINTHELLO: LDM 1, 2 and make jumping to them work

newLines = []
#i = 0 # The current line
#p = 0 # The current line
linesWithoutJMPShorts = []

i = 0
for j in lines: #For managing jmpShortcuts    
    if j[-1] != ':': linesWithoutJMPShorts.append(j)
    else: jmpShortcuts[j[:-1]] = i; continue
    i += 1

for i, j in enumerate(linesWithoutJMPShorts):
    ##Find jumpShortcuts and store them in the dictionary 'jmpShortcuts'
    #if j[-1] == ':':#'{': #Find last character
    #    jmpShortcuts[j[:-1]] = i#[i] # Make an item in the dictionary named (the line without the last character) with value of the current line(i)
    #    continue
    
    #THE OLD SYSTEM FOR FUNCTION THAT WONT WORK
    #if j.count("}") != 0: 
    #    for k in range(j.count("}")):
    #        for key, value in jmpShortcuts.items():
    #            print(value)
    #            if len(value) < 2: jmpShortcuts[key].append(i); break #Continue so we can start the loop from the front with the next bracket
    #        else: print(f"ERROR AT LINE {i}: The curly brace '}}' couldn't find it's pair '{{'"); exit()# the braces are doubled because otherwise it gives error and we exit because the loop cant be stopped
    #    continue
    
    lineItems = re.split(' ,|, |,| |\|', j) #Split on " ," or ", " or "," or " "
    lineItems2 = []
    
    if   lineItems[0].upper() == 'NOP': continue #Nop doesn't count as a line
    elif lineItems[0].upper() == 'ADD':
        if(len(lineItems[1]) > 3 or len(lineItems[2]) > 3 or len(lineItems) != 3): print(f"ERROR AT LINE {i}: The usage of 'ADD' is [ADD reg, reg]"); exit()
        lineItems2.append('01')
        lineItems2.append((hex(int(lineItems[1], 16))[2:]))
        lineItems2.append((hex(int(lineItems[2], 16))[2:]))
        lineItems2.append('00')
    elif lineItems[0].upper() == 'SUB':
        if(len(lineItems[1]) > 3 or len(lineItems[2]) > 3 or len(lineItems) != 3): print(f"ERROR AT LINE {i}: The usage of 'SUB' is [SUB reg, reg]"); exit()
        lineItems2.append('02')
        lineItems2.append((hex(int(lineItems[1], 16))[2:]))
        lineItems2.append((hex(int(lineItems[2], 16))[2:]))
        lineItems2.append('00')
    elif lineItems[0].upper() == 'NND':
        if(len(lineItems[1]) > 3 or len(lineItems[2]) > 3 or len(lineItems) != 3): print(f"ERROR AT LINE {i}: The usage of 'NND' is [NND reg, reg]"); exit()
        lineItems2.append('03')
        lineItems2.append((hex(int(lineItems[1], 16))[2:]))
        lineItems2.append((hex(int(lineItems[2], 16))[2:]))
        lineItems2.append('00')
    elif lineItems[0].upper() == 'CMP':
        if(len(lineItems[1]) > 3 or len(lineItems[2]) > 3 or len(lineItems) != 3): print(f"ERROR AT LINE {i}: The usage of 'CMP' is [CMP reg, reg]"); exit()
        lineItems2.append('04')
        lineItems2.append((hex(int(lineItems[1], 16))[2:]))
        lineItems2.append((hex(int(lineItems[2], 16))[2:]))
        lineItems2.append('00')
    elif lineItems[0].upper() == 'JMP':
        lineItems2.append('05')
        lineItems2.append('00')
        
        if lineItems[1] in jmpShortcuts: lineItems2.append(format(int(hex(jmpShortcuts.get(lineItems[1])), 16), '02X'))#)[0]), 16), '02X')) #Use the dictionary if needed
        elif lineItems[1] not in jmpShortcuts:
            try: 
                if len(lineItems[1]) <= 4 and len(lineItems) == 2: 
                    lineItems2.append(format(int(lineItems[1], 16), '02X'))
                else: print(f"ERROR AT LINE {i}: The usage of 'JMP' is [JMP mem(8bit)] or [JMP string(jmpShortcut)]"); exit()
            except: print(f"ERROR AT LINE {i}: The jmp shortcut {lineItems[1]} is not defined in the dictionary"); exit()
    elif lineItems[0].upper() == 'JGT':
        lineItems2.append('06')
        lineItems2.append('00')
        
        if lineItems[1] in jmpShortcuts: lineItems2.append(format(int(hex(jmpShortcuts.get(lineItems[1])), 16), '02X'))#)[0]), 16), '02X')) #Use the dictionary if needed
        elif lineItems[1] not in jmpShortcuts:
            try: 
                if len(lineItems[1]) <= 4 and len(lineItems) == 2: 
                    lineItems2.append(format(int(lineItems[1], 16), '02X'))
                else: print(f"ERROR AT LINE {i}: The usage of 'JGT' is [JGT mem(8bit)] or [JGT string(jmpShortcut)]"); exit()
            except: print(f"ERROR AT LINE {i}: The jmp shortcut {lineItems[1]} is not defined in the dictionary"); exit()
    elif lineItems[0].upper() == 'JIE':
        lineItems2.append('07')
        lineItems2.append('00')
        
        if lineItems[1] in jmpShortcuts: lineItems2.append(format(int(hex(jmpShortcuts.get(lineItems[1])), 16), '02X'))#)[0]), 16), '02X')) #Use the dictionary if needed
        elif lineItems[1] not in jmpShortcuts:
            try: 
                if len(lineItems[1]) <= 4 and len(lineItems) == 2: 
                    lineItems2.append(format(int(lineItems[1], 16), '02X'))
                else: print(f"ERROR AT LINE {i}: The usage of 'JIE' is [JIE mem(8bit)] or [JIE string(jmpShortcut)]"); exit()
            except: print(f"ERROR AT LINE {i}: The jmp shortcut {lineItems[1]} is not defined in the dictionary"); exit()
    elif lineItems[0].upper() == 'JLT':
        lineItems2.append('08')
        lineItems2.append('00')
        
        if lineItems[1] in jmpShortcuts: lineItems2.append(format(int(hex(jmpShortcuts.get(lineItems[1])), 16), '02X'))#)[0]), 16), '02X')) #Use the dictionary if needed
        elif lineItems[1] not in jmpShortcuts:
            try: 
                if len(lineItems[1]) <= 4 and len(lineItems) == 2: 
                    lineItems2.append(format(int(lineItems[1], 16), '02X'))
                else: print(f"ERROR AT LINE {i}: The usage of 'JLT' is [JLT mem(8bit)] or [JLT string(jmpShortcut)]"); exit()
            except: print(f"ERROR AT LINE {i}: The jmp shortcut {lineItems[1]} is not defined in the dictionary"); exit()
    elif lineItems[0].upper() == 'SRV':
        if(len(lineItems[1]) > 3 or len(lineItems[2]) > 5 or len(lineItems) != 3): print(f"ERROR AT LINE {i}: The usage of 'SRV' is [SRV reg, reg + mem(12bit)]"); exit()
        lineItems2.append('09')
        lineItems2.append((hex(int(lineItems[1], 16))[2:]))
        lineItems2.append(format(int(lineItems[2], 16), '03X'))
    elif lineItems[0].upper() == 'CPR':
        if(len(lineItems[1]) > 3 or len(lineItems[2]) > 3 or len(lineItems) != 3): print(f"ERROR AT LINE {i}: The usage of 'CPR' is [CPR reg, reg]"); exit()
        lineItems2.append('0a')
        lineItems2.append((hex(int(lineItems[1], 16))[2:]))
        lineItems2.append((hex(int(lineItems[2], 16))[2:]))
        lineItems2.append('00')
    elif lineItems[0].upper() == 'RCL':
        if(len(lineItems[1]) > 3 or len(lineItems) != 2): print(f"ERROR AT LINE {i}: The usage of 'RCL' is [RCL reg]"); exit()
        lineItems2.append('0b')
        lineItems2.append((hex(int(lineItems[1], 16))[2:]))
        lineItems2.append('000')
    elif lineItems[0].upper() == 'MCL':
        if(len(lineItems[1]) > 3 or len(lineItems) != 2): print(f"ERROR AT LINE {i}: The usage of 'MCL' is [MCL reg(as ROMMemAddres)"); exit()
        lineItems2.append('0c')
        lineItems2.append((hex(int(lineItems[1], 16))[2:]))
        lineItems2.append('000')
    elif lineItems[0].upper() == 'LDM':
        if(len(lineItems[1]) > 3 or len(lineItems[2]) > 3 or len(lineItems) != 3): print(f"ERROR AT LINE {i}: The usage of 'LDM' is [LDM reg(as ROMMemAddres), reg]"); exit()
        lineItems2.append('0d')
        lineItems2.append((hex(int(lineItems[1], 16))[2:]))
        lineItems2.append((hex(int(lineItems[2], 16))[2:]))
        lineItems2.append('00')
    elif lineItems[0].upper() == 'LDR':
        if(len(lineItems[1]) > 3 or len(lineItems[2]) > 3 or len(lineItems) != 3): print(f"ERROR AT LINE {i}: The usage of 'LDR' is [LDR reg(as ROMMemAddres), reg]"); exit()
        lineItems2.append('0e')
        lineItems2.append((hex(int(lineItems[1], 16))[2:]))
        lineItems2.append((hex(int(lineItems[2], 16))[2:]))
        lineItems2.append('00')
    elif lineItems[0].upper() == 'SMV':
        if(len(lineItems[1]) > 3 or len(lineItems[2]) > 5 or len(lineItems) != 3): print(f"ERROR AT LINE {i}: The usage of 'SMV' is [SMV reg(as ROMMemAddres), reg + mem(12Bit)]"); exit()
        lineItems2.append('0f')
        lineItems2.append((hex(int(lineItems[1], 16))[2:]))
        lineItems2.append(format(int(lineItems[2], 16), '03X'))
    elif lineItems[0].upper() == 'SPC':
        if(len(lineItems[1]) != 5 or len(lineItems[2]) != 6 or len(lineItems[3]) != 5 or len(lineItems) != 4): print(f"ERROR AT LINE {i}: The usage of 'SPC' is [SPC R(5bitBinary), G(6bitBinary), B(5bitBinary)]"); exit()
        lineItems2.append('10') #Here is kind of bad with the coloring
        #lineItems2.append((hex(int(lineItems[1], 16))[2:]))
        ##lineItems2.append((hex(int(lineItems[2], 16))[2:]))
        #lineItems2.append(format(int(lineItems[2], 16), '02X'))
        #lineItems2.append((hex(int(lineItems[3], 16))[2:]))
        
        lineItems2.append(format(int(lineItems[1] + lineItems[2] + lineItems[3], 2), '04X'))
    elif lineItems[0].upper() == 'DWP':
        if(len(lineItems[1]) > 3 or len(lineItems[2]) > 3 or len(lineItems) != 3): print(f"ERROR AT LINE {i}: The usage of 'DWP' is [DWP reg(X), reg(Y)]"); exit()
        lineItems2.append('11')
        lineItems2.append((hex(int(lineItems[1], 16))[2:]))
        lineItems2.append((hex(int(lineItems[2], 16))[2:]))
        lineItems2.append('00')
    elif lineItems[0].upper() == 'HLT':
        if(len(lineItems) != 1): print(f"ERROR AT LINE {i}: The usage of 'HLT' is [HLT]"); exit()
        lineItems2.append('12')
        lineItems2.append('0000')
    else: print(f"ERROR AT LINE {i}: The OPCode '{lineItems[0]}' is invalid"); exit()
    
    print(lineItems2)
    newLines.append(''.join(lineItems2))
    #i += 1 # Update the current line
#print(newLines)
print(' '.join(newLines)) #Print without parentheses and commas
os.system("Pause")
