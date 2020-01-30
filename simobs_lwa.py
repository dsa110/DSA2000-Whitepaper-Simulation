#!/usr/bin/env python
import casatasks
import casatools
import sys
import os.path

# set up
msname='sim_output.ms'
conf_file='LWA_coordinates.cfg'
if len(sys.argv) > 1:
    fitsimage = sys.argv[1]
else:
    fitsimage = 'SKAMid_B2_8h_v3.fits'

assert os.path.exists(fitsimage)
assert 'fits' in fitsimage
image = fitsimage.replace('.fits', '.image')
if not os.path.exists(image):
    print('creating ms image to be used as sky model')
    im = casatools.image()
    im.fromfits(infile=fitsimage, outfile=image)

# get antenna positions
tabname='antenna_positions_'+conf_file.split('.cfg')[0]+'.tab'
tb = casatools.table()
tb.fromascii(tabname, conf_file, firstline=3, sep=' ', columnnames=['X', 'Y', 'Z', 'DIAM', 'NAME'], datatypes=['D', 'D', 'D', 'D', 'A'])
xx=tb.getcol('X')
yy=tb.getcol('Y')
zz=tb.getcol('Z')
diam=tb.getcol('DIAM')
anames=tb.getcol('NAME')
tb.close()

# simulate setup
sm = casatools.simulator()
me = casatools.measures()
sm.open(msname)
sm.setconfig(telescopename='ovro_mma', x=xx, y=yy, z=zz, dishdiameter=diam, mount='alt-az', antname=list(anames), padname=list(anames), coordsystem='global')
sm.setspwindow(spwname='LWABand', freq='35MHz', deltafreq='21kHz', freqresolution='21kHz', nchannels=2398, stokes='XX XY YX YY')
sm.setfeed('perfect X Y')
# With rotated.cfg I got 6.11x6.02 with natural weighting.
# sm.setfield(sourcename='source', sourcedirection=['J2000', '00h00m0.0', '+85.00.00.000'])
# declination from wsclean
sm.setfield(sourcename='source', sourcedirection=['J2000', '00h00m0.0', '+37.14.02.000'])
sm.setauto(autocorrwt=0.0)

# simulate time
sm.setlimits(shadowlimit=0.001, elevationlimit='8.0deg')
integrationtime='10s'
sm.settimes(integrationtime=integrationtime, usehourangle=True, referencetime=me.epoch('utc', '58562.0d'))
startha='-5s'
endha='5s'
sm.setoptions(ftmachine='ft')
sm.observe('source', 'LWABand', starttime=startha, stoptime=endha)

# simulate sky model
#sm.predict(imagename=image)
sm.setnoise(mode='simplenoise', simplenoise='1Jy')
sm.corrupt()
