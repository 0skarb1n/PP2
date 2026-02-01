# skip banana
f=["apple","banana","cherry"]
for x in f:
  if x=="banana":
    continue
  print(x)

# skip 3
for x in range(6):
  if x==3:
    continue
  print(x)

# skip odds
for x in range(10):
  if x%2!=0:
    continue
  print(x)

# skip letter o
for x in "hello world":
  if x=="o":
    continue
  print(x)

# skip small nums
nums=[10,20,3,40,5]
for x in nums:
  if x<10:
    continue
  print(x)