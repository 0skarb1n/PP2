# using AND: returns True if both statements are true
x = 5
print(x > 3 and x < 10)

# using OR: returns True if one of the statements is true
x = 5
print(x > 3 or x < 4)

# using NOT: reverse the result
x = 5
print(not(x > 3 and x < 10))

# combining AND in an if statement
a = 200
b = 33
c = 500
if a > b and c > a:
  print("Both conditions are True")

# combining OR in an if statement
if a > b or a > c:
  print("At least one of the conditions is True")