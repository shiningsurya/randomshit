import pytz
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
start = pytz.timezone('UTC').localize( dt.datetime(2019,1,1) )
oneminute = dt.timedelta(minutes=1)
oneday    = dt.timedelta(days=1)
ltz = np.array(pytz.common_timezones)
ntz = len(ltz)
mins = np.arange(1440)
days = [68,79,263,306]
# days = [68,69]
outp = 'paint3_6869.png'
mat = np.zeros((ntz,mins.size),dtype=np.bool)
fourtwozero = lambda x : True if x.hour in [4,16] and x.minute == 20 else False
###
lap = []
###
for iday, day in enumerate(days):
    istart = start + day * oneday
    for imi in mins:
        for itz, tz in enumerate(ltz):
            iistart = istart.astimezone(pytz.timezone(tz))
            if fourtwozero(iistart):
                mat[itz,imi] = True
        istart = istart + oneminute
    perday = mat.sum(0)
    paint1 = np.array([ ltz[mat[:,imi]] for imi in mins])
    emind = [img for img,xim in enumerate(paint1) if 0 in xim.shape]
    paint1 = np.delete(paint1, emind)
    lap.append(perday)
###
# 875 is super max
clrs = np.random.randint(0,255,size=(875,3))
clrs = ['#{:02x}{:02x}{:02x}'.format(r,g,b) for r,g,b in clrs]
from itertools import cycle
colors = cycle(clrs)
import geopandas as gpd
sf = gpd.read_file('./dist/combined-shapefile.shp')
# plot
fig, ax = plt.subplots(1,1,sharex=True,sharey=True,figsize=(5,5),dpi=300)
plt.sca(ax)
plt.plot(lap[1]-lap[0])
plt.xlabel('Minute of day')
plt.ylabel('Diff')
plt.title(str(days[0]) + '-' + str(days[1]))
plt.tight_layout()
plt.savefig(outp)
