import re

txt ="The rain in Spain"

x=re.search("Spain$",txt)

if x:
  print("YES! We have a match!")
else:
  print("No match")
