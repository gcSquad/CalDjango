import pytz
import datetime
from django.utils import timezone

def return_dates_in_isoformat(days_delta,operator):

        tz = pytz.timezone('Asia/Kolkata')
        if operator == 'add':
            required_datetime = timezone.now()+datetime.timedelta(days=days_delta)
        elif operator == 'subtract':
            required_datetime = timezone.now()-datetime.timedelta(days=days_delta)

        date_in_required_format = required_datetime.replace(microsecond=0).isoformat()
        return date_in_required_format 