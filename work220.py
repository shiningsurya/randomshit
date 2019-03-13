import pytz
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
start = pytz.timezone('UTC').localize( dt.datetime(2019,1,1) )
oneminute = dt.timedelta(minutes=1)
ltz = np.array(pytz.common_timezones)
ntz = len(ltz)
mins = np.arange(1440)
days = np.arange(365)
mat = np.zeros((days.size,ntz,mins.size),dtype=np.bool)
#
fourtwozero = lambda x : True if x.hour in [4,16] and x.minute == 20 else False
## WORK LOOP 2
istart = start
for day in days:
    for imi in mins:
        for itz, tz in enumerate(ltz):
            iistart = istart.astimezone(pytz.timezone(tz))
            if fourtwozero(iistart):
                mat[day,itz,imi] = True
        istart = istart + oneminute
