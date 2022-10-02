import os

def sgn(num):
    if num > 0:
        return 1
    elif num < 0:
        return -1
    else:
        return 0
def convert_to_hex(number:int):
    if number == None:
        return "Invalid input"
    elif type(number) == float:
        return "Float not handled"
    elif type(number) == str:
        temp = int(number)
        return format(temp, "02x")
    return format(number, '02x')
Ax = input("X value of point A in hex: ")#"7F"
Ay = input("Y value of point A in hex: ")#"7F"
Bx = input("X value of point B in hex: ")#"00"
By = input("Y value of point B in hex: ")#"00"

Ax = int(Ax, 16)
Ay = int(Ay, 16)
Bx = int(Bx, 16)
By = int(By, 16)

incX = sgn(Bx - Ax)
dX = abs(Bx - Ax)

incY = sgn(By - Ay)
dY = abs(By - Ay)

XaY = dX > dY
cmpt = max(dX, dY)
incD = -2*abs(dX - dY)
incS =  2*min(dX, dY)

err = incD + cmpt
X = Ax
Y = Ay

#while cmpt >= 0:
#    print(f"{X}, {Y}")
#    cmpt -= 1
#    if err >= 0 or XaY:
#        X += incX
#    if err >= 0 or not XaY:
#        Y += incY
#    if err >= 0:
#        err += incD
#    else:
#        err += incS
#while cmpt >= 0:
#    print(f"{X}, {Y}")
#    cmpt -= 1
#    if XaY:
#        X += incX
#    if not XaY:
#        Y += incY
#    if err >= 0:
#        X += incX
#        Y += incY
#        err += incD
#    else:
#        err += incS
#
i = 1
while cmpt >= 0:
    print(f"Loop Number {i}")
    print(f"Reg0 | {convert_to_hex(incX)}")
    print(f"Reg1 | {convert_to_hex(dX)}")
    print(f"Reg2 | {convert_to_hex(incY)}")
    print(f"Reg3 | {convert_to_hex(dY)}")
    print(f"Reg4 | {convert_to_hex(XaY)}")
    print(f"Reg5 | {convert_to_hex(cmpt)}")
    print(f"Reg6 | {convert_to_hex(incD)}")
    print(f"Reg7 | {convert_to_hex(incS)}")
    print(f"Reg8 | {convert_to_hex(err)}")
    print(f"Reg9 | {convert_to_hex(X)}")
    print(f"RegA | {convert_to_hex(Y)}")
    
    cmpt -= 1
    i+=1
    
    if err >= 0 or XaY:
        X += incX
    if err >= 0 or not XaY:
        Y += incY
    if err >= 0:
        err += incD
    else:
        err += incS
os.system("pause")