import numpy as np
from astropy.io import fits
from scipy.io.wavfile import write
import sys
if len(sys.argv) <= 1:
    print "Usage: {0} <path-to-file> <output-wav-file>".format(sys.argv[0])
    sys.exit(0)
huh = fits.open(sys.argv[1])
#########
hnames = [x.name for x in huh]
pparam = huh[ hnames.index('PSRPARAM') ]
sint = huh[ hnames.index('SUBINT') ]
phdu = huh[ hnames.index('PRIMARY') ]
ppdat = pparam.data['PARAM']
##
# Take data from subint
# observation freq from phdu
# period from psrparam
# do i actually need obsfreq?
##
for i in ppdat:
    ii = i.split()
    if ii[0] == 'F0':
        f0 = float(ii[1])
#
sdat = sint.data['DATA']
ip = sdat[0,0,0]
############### ip, f0
#### summing sinesoids
rip = np.roll(ip, ip.size//2 - ip.argmax())
tm = 2.0
# t = np.linspace(0,tm,44100*2)
t = np.arange(0, tm, 1/44100.)
ret = np.zeros(t.size)
freq = np.linspace(20, 20e3, rip.size)
for i, f in enumerate(freq):
    ret = ret + rip[i] * np.cos(2*np.pi*f*t)
np.savetxt('test.dat', ret, fmt='%0.3f')
sl = lambda x : np.int16( (x / np.max(np.abs(x))) * 32767)
write(sys.argv[2], 44100 , sl(ret))
