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
outp = "four_/"
#
fourtwozero = lambda x : True if x.hour in [4,16] and x.minute == 20 else False
## WORK LOOP 4
istart = start
for imi in mins:
    for itz, tz in enumerate(ltz):
        iistart = istart.astimezone(pytz.timezone(tz))
        if fourtwozero(iistart):
            mat[itz,imi] = True
    istart = istart + oneminute

paint1 = np.array([ ltz[mat[:,imi]] for imi in mins])
emind = [img for img,xim in enumerate(paint1) if 0 in xim.shape]
nzmins =[mins[i] for i in mins if not 0 in paint1[i].shape] 
paint1 = np.delete(paint1, emind)
####
#
###
clr = 'g'
import geopandas as gpd
sf = gpd.read_file('./dist/combined-shapefile.shp')
for imin, imi in enumerate(nzmins):
    fig = plt.figure(figsize=(20,10),dpi=300)
    ax = plt.gca()
    sf.plot(ax=ax,color='', edgecolor='k')
    ii = sf[sf['tzid'].isin(paint1[imin])]
    ii.plot(ax=ax,color=clr,edgecolor='')
    plt.xlim( (-180,180)  )
    plt.ylim( (-90,90)  )
    plt.xticks()
    plt.yticks()
    plt.tight_layout()
    outpp = outp + str(imi) + '.png'
    plt.savefig(outpp)
    plt.close()
###
