# standard if-elif-else
a = 200
b = 33
if b > a:
  print("b is greater than a")
elif a == b:
  print("a and b are equal")
else:
  print("a is greater than b")

# checking multiple conditions
x = 10
if x > 20:
  print("More than 20")
elif x > 5:
  print("More than 5 but less than 20")
else:
  print("Less than 5")

# simple grade checker  ddd
score = 75
if score >= 90:
  print("Grade A")
elif score >= 70:
  print("Grade B")
else:
  print("Grade C")

# checking strict equality
status = "loading"
if status == "error":
  print("Something broke")
elif status == "loading":
  print("Please wait")
else:
  print("Ready")

# number comparison
num = 0
if num > 0:
  print("Positive number")
elif num < 0:
  print("Negative number")
else:
  print("It is zero")