import math
import numpy as np

def Srotate(angle, valuex, valuey, pointx, pointy):
    valuex = np.array(valuex)
    valuey = np.array(valuey)
    sRotatex = (valuex - pointx) * math.cos(angle) + (valuey - pointy) * math.sin(angle) + pointx
    sRotatey = (valuey - pointy) * math.cos(angle) - (valuex - pointx) * math.sin(angle) + pointy
    return sRotatex, sRotatey

x1 = eval(input('x1 = '))
y1 = eval(input('y1 = '))
x2 = eval(input('x2 = '))
y2 = eval(input('y2 = '))
rot = eval(input('rot = '))

arr = [(x1,y1),(x1,y2),(x2,y1),(x2,y2)]
print("box的四个坐标分别为：")
for n in range(4):
        print(arr[n])

arr1 =[]
print("旋转后的的四个坐标分别为：")
for n in range(4):
    sPointx, sPointy = Srotate(math.radians(rot), arr[n][0], arr[n][1], (x1 + x2) / 2, (y1 + y2) / 2)
    arr1.append([sPointx, sPointy])
    print('this number is{}'.format(arr1[n]))
