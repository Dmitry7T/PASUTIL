from datetime import datetime
import pytz

def time_is_good():
    zone = pytz.timezone('Europe/London')

    now = datetime.now(zone)

    day = now.strftime("%A") 

    if day != 'Saturday' and day != 'Sunday':
        return True
    else:
        return False
