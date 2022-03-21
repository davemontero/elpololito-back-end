from datetime import datetime

strdate = datetime.strptime('2000-01-01', '%Y-%m-%d')
print(strdate)
print(strdate.date())
print(datetime.now().date())

