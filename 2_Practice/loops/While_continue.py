# skip 3
i=0
while i<6:
  i+=1
  if i==3:
    continue
  print(i)

# skip evens
i=0
while i<10:
  i+=1
  if i%2==0:
    continue
  print(i)

# skip specific
x=0
while x<5:
  x+=1
  if x==2:
    continue
  print(x)

# multiple skips
i=0
while i<6:
  i+=1
  if i==2 or i==4:
    continue
  print(i)

# countdown skip
c=6
while c>0:
  c-=1
  if c==3:
    continue
  print(c)