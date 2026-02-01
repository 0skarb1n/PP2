# one line if statement
if 200 > 33: print("200 is greater than 33")

# one line comparison
a = 50
b = 10
if a > b: print("a is greater")

# short hand if-else (ternary operator)
a = 2
b = 330
print("A") if a > b else print("B")

a = 330
b = 330
print("A") if a > b else print("=") if a == b else print("B")

# assigning value based on condition
age = 18
status = "Adult" if age >= 18 else "kid"
print(status)