import datetime as dt  
import pytz

date_time_str = "2019-07-03 12:00:00+00:00"
date_time_str = date_time_str[:-6]

# returndate=datetime.datetime(datetime_str).utcnow().isoformat() + 'Z'
#x=datetime.datetime.utcnow().isoformat() + 'Z'
date_time_obj = dt.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
x=date_time_obj.isoformat()
print(x)