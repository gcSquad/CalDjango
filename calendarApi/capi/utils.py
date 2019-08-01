import datetime
from django.utils import timezone
import dateutil.parser
from dateutil import tz
import pytz


def return_dates_in_isoformat(days_delta,operator):
      
        if operator == 'add':
            required_datetime = timezone.now()+datetime.timedelta(days=days_delta)
        elif operator == 'subtract':
            required_datetime = timezone.now()-datetime.timedelta(days=days_delta)

        date_in_required_format = required_datetime.replace(microsecond=0).isoformat()
        return date_in_required_format 

def convert_into_local_timezone(utc_time,timezone):
    to_zone = tz.gettz(timezone)
    from_zone = tz.gettz('UTC')
    utc_datetime_object=dateutil.parser.parse(utc_time)
    return (utc_datetime_object.replace(tzinfo=from_zone).astimezone(to_zone)).isoformat()

