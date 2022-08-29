#!/usr/bin/env python
'''
Module to query a local copy of the NOMAD1 catalog
'''

import re
import astropy.units as u
from astropy.coordinates import SkyCoord
from astroquery.gaia import Gaia
from collections import namedtuple

GaiaStar = namedtuple('GaiaStar', 'id radec bmag rmag')

def _convert_mag(mag_str):
    if '---' in mag_str:
        return None
    m = re.match('([\d\.]+)', mag_str)
    return float(m.groups()[0])
    

def query(ra, dec, radius_arcsec, catalog_table='gaiadr3.gaia_source', max=None, mag={}):
    '''Query the GAIA DR3 catalog

    Parameters
    ----------
    ra: float
        Right Ascension angle in degrees
    dec: float
        Declination angle in degrees
    radius_arcsec: float
        search radius in arcsec
    max: int, optional
        max number of stars to return, default 1000
    mag: dict
        magnitude min,max limits. Example: {'R':(10,15), 'V':(12, 17)}

    catalog_table: string, optional
        GAIA data source
    '''
    max = max or 1000

    coord = SkyCoord(ra=ra*u.degree, dec=dec*u.degree, frame='icrs')
    r = Gaia.query_object(coord, radius=radius_arcsec/3600*u.degree)

    stars = []
    for line in r:

        designation = line['DESIGNATION']
        ra = line['ra']
        dec = line['dec']
        Bmag = line['phot_bp_mean_mag']
        Rmag = line['phot_rp_mean_mag']

        radec = '%011.8f%011.8f' % (ra, dec)
        for m in mag:
            if m == 'B':
                mag_min = mag[m][0]
                mag_max = mag[m][1]
                if Bmag < mag_min or Bmag > mag_max:
                    continue
            elif m == 'R':
                mag_min = mag[m][0]
                mag_max = mag[m][1]
                if Rmag < mag_min or Rmag > mag_max:
                    continue
            else:
                raise ValueError('Magnitude band %s not available in Gaia catalog' % m)
            
        stars.append(GaiaStar(designation, radec, Bmag, Rmag))

    return stars

