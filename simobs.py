conf_file='dsa2000-loc.cfg'
tabname='antenna_positions_'+conf_file.split('.cfg')[0]+'.tab'
tb.fromascii(tabname, conf_file, firstline=3, sep=' ', columnnames=['X', 'Y', 'Z', 'DIAM', 'NAME'], datatypes=['D', 'D', 'D', 'D', 'A'])
xx=tb.getcol('X')
yy=tb.getcol('Y')
zz=tb.getcol('Z')
diam=tb.getcol('DIAM')
anames=tb.getcol('NAME')
tb.close()

ms_name='DSA_2000_ant_10s_mma_SKAMid_bright.ms'

sm.open(ms_name)
pos_ovro_mma=me.observatory('ovro_mma')
sm.setconfig(telescopename='ovro_mma', x=xx, y=yy, z=zz, dishdiameter=diam, mount='alt-az', antname=list(anames), padname=list(anames), coordsystem='local', referencelocation=pos_ovro_mma)
sm.setspwindow(spwname='LBand', freq='0.7GHz', deltafreq='10MHz', freqresolution='10MHz', nchannels=130, stokes='RR RL LR LL')
sm.setfeed('perfect R L')
# With rotated.cfg I got 6.11x6.02 with natural weighting.
# sm.setfield(sourcename='source', sourcedirection=['J2000', '00h00m0.0', '+85.00.00.000'])
# declination from wsclean
sm.setfield(sourcename='source', sourcedirection=['J2000', '00h00m0.0', '+37.07.47.400'])

sm.setlimits(shadowlimit=0.001, elevationlimit='8.0deg')
integrationtime='10s'
sm.setauto(autocorrwt=0.0)
sm.settimes(integrationtime=integrationtime, usehourangle=True, referencetime=me.epoch('utc', '58562.0d'))
startha='-5s'
endha='5s'
sm.setoptions(ftmachine='ft')
sm.observe('source', 'LBand', starttime=startha, stoptime=endha)
sm.predict(imagename='SKAMid_B1_100h_v3_scaled_cropped_bright.image')
#sm.setnoise(mode='simplenoise', simplenoise='8uJy')
#sm.corrupt()
