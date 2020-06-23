import os
from datetime import datetime
from datetime import date, timedelta

now = datetime.now().time()
date = date.today()

print (now)
print(date)

Ts = timedelta(hours = 0, minutes = 0, seconds = 0)
print(Ts)
now = datetime.now()
Ts += timedelta(hours=now.hour, minutes=now.minute, seconds=now.second)
print(str(Ts))