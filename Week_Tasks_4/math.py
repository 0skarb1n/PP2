import math
#First
d=int(input("input degree:"))
radian = d*3.14/180
print(f"output Radian: {radian}")
#Second
hei=int(input("input height:"))
Base1=int(input("Base, first value:"))
Base2=int(input("Base, second value:"))
area = (Base1+Base2)*hei/2
print(f"Outpud area: {area}")
#Third
sides = int(input("input number of sides:"))
length = int(input("input length of a side:"))
area = (sides*length**2)/(4*math.tan(math.pi/sides))
print(f"Output area: {area}")
#fouth parrolologramm
length = int(input("Lenght of base:"))
height = int(input("Height of parallelogram:"))
area = length*height
print(f"Output area: {area}")
