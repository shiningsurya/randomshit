# coding: utf-8
import pytz
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
start = pytz.timezone('UTC').localize( dt.datetime(2019,1,1) )
oneminute = dt.timedelta(minutes=1)
ltz = np.array(pytz.common_timezones)
ntz = len(ltz)
mins = np.arange(1440)
mat = np.zeros((ntz,mins.size),dtype=np.bool)
#
fourtwozero = lambda x : True if x.hour in [4,16] and x.minute == 20 else False
## WORK LOOP 1
istart = start
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
####
#
###
def plot_paint1():
    clrs = np.random.randint(0,255,size=(paint1.size,3))
    clrs = ['#{:02x}{:02x}{:02x}'.format(r,g,b) for r,g,b in clrs]
    colors = iter(clrs)
    import geopandas as gpd
    sf = gpd.read_file('./dist/combined-shapefile.shp')
    fig = plt.figure(figsize=(20,10),dpi=300)
    ax = plt.gca()
    # sf.plot(ax=ax,color='white', edgecolor='black')
    for xi in paint1:
        ii = sf[sf['tzid'].isin(xi)]
        ii.plot(ax=ax,color=next(colors),edgecolor='')
    ####
    plt.xlim( (-180,180)  )
    plt.ylim( (-90,90)  )
    plt.xticks()
    plt.yticks()
    plt.tight_layout()
    plt.savefig('paint1.png')
###
