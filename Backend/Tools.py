from datetime import datetime
import pytz
def convert_date(ts):
    timestamp = ts/1000.0
    date_obj = datetime.fromtimestamp(timestamp)
    # Filter By time to Avoid sending Alerts at bad time of the day 
    # From 8:00 AM to 16:00 PM
    formated_date = date_obj.strftime('%S  %Z %z')
    return str(formated_date)