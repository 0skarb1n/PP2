#first generator
N = int(input("N number:"))
def generator(n):
    for i in range(n):
        yield i**2

for value in generator(N):
    print(value)
#second generator
def generator2(n):
    for i in range(n):
        if(i%2==0):
            yield str(i)

print(",".join(generator2(N)))
#third generator
def generator3(n):
    for i in range(n):
        if(i%12==0):
            yield str(i)

print(",".join(generator3(N)))
#FOURTH GENERATOR
a=int(input("A number:"))
b=int(input("B number:"))
def squares(a,b):
    for i in range(a,b+1):
        yield str(i**2)

print(",".join(squares(a,b)))

#Fifth generator
N = int(input("N number:"))
def generator4(n):
    for i in range(n,0,-1):
        yield i

for value in generator4(N):
    print(value, end=" ")
