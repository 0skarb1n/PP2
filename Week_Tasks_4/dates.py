from datetime import datetime, timedelta
#First
today = datetime.now()
print (today)
print("Five days from now:", today + timedelta(days=5))
#Second
print("Yesterday:", today - timedelta(days=1))
print("Tomorrow:", today + timedelta(days=1))
#Third
microseconds = today.microsecond
print("Microseconds:", microseconds)
print("without microseconds:", today.replace(microsecond=0))
#Fourth
date2 = today + timedelta(days=5)
print("Difference between two dates in seconds:", (date2 - today).total_seconds())
