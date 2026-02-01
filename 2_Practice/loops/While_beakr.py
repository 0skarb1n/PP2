# stop at 3
i=1
while i<6:
  print(i)
  if i==3:
    break
  i+=1

# break before print
i=1
while i<6:
  if i==3:
    break
  print(i)
  i+=1

# find target
t=5
c=0
while c<10:
  if c==t:
    break
  c+=1

# inf loop break
x=10
while True:
  x-=1
  if x==0:
    break

# calc break
n=1
while n<100:
  if n*2>50:break
  n+=1