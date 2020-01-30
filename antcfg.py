from astropy.io import ascii
import astropy.coordinates as ac
from astropy.table import Table

# first export xlsx to csv
# remove some of header so only one line left above data

# read csv
tab = ascii.read('LWA352_tmp.csv', delimiter=',', data_start=1)

# parse values to WGS84
xx = [] 
yy = [] 
zz = [] 
names = [] 
for name, lat, lon in tab[['col2', 'col3', 'col4']]:   # may need to adjust cols to use
    print(name, lon, lat) 
    loc = ac.EarthLocation.from_geodetic(lon=lon, lat=lat)   # default uses WGS84
    xx.append(loc.x.value) 
    yy.append(loc.y.value) 
    zz.append(loc.z.value) 
    names.append(name)

# write out WGS84 values
tab = Table([xx, yy, zz, [0]*len(xx), names], names=['x', 'y', 'z', 'diam', 'name']) 
tab.write('LWA352_tmp.cfg', format='ascii')
