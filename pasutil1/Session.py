import datetime 
import time

def is_London():
    return datetime.time(11, 0) <= datetime.datetime.now().time() <= datetime.time(18, 30) \
                and datetime.datetime.now().weekday() < 5