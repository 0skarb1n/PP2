# break on banana
f=["apple","banana","cherry"]
for x in f:
  print(x)
  if x=="banana":break

# break before
f=["apple","banana","cherry"]
for x in f:
  if x=="banana":break
  print(x)

# range break
for x in range(6):
  if x==3:break
  print(x)

# find num
nums=[1,5,12,20,3]
for n in nums:
  if n>10:break

# sum limit
t=0
for x in range(10):
  t+=x
  if t>15:break