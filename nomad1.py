#!/usr/bin/env python
'''
Module to query a local copy of the NOMAD1 catalog
'''

import re
import subprocess
from collections import namedtuple

from catalog_conf import nomad1_exe, nomad1_dir


NOMAD1Star = namedtuple('NOMAD1Star', 'radec bmag vmag rmag jmag hmag kmag R')

def _convert_mag(mag_str):
    if '---' in mag_str:
        return None
    m = re.match('([\d\.]+)', mag_str)
    return float(m.groups()[0])
    

def query(ra, dec, radius_arcsec, catalog_dir=None, exefile=None, max=None, mag={}):
    '''Query the NOMAD1 catalog

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

    catalog_dir: string, optional
        directory with NOMAD1 data files
    exefile: string, optional
        NOMAD1 search program
    '''
    exefile = exefile or nomad1_exe
    catalog_dir = catalog_dir or nomad1_dir
    max = max or 1000

    if dec>=0:
       radec = '%f+%f' % (ra, dec)
    else:
       radec = '%f%f' % (ra, dec)

    args = []
    args.append(exefile)
    args.append('-R')
    args.append(catalog_dir)
    args.append('-c')
    args.append(radec)
    args.append('-rs')
    args.append(str(radius_arcsec))
    args.append('-m')
    args.append(str(max))

    for m in mag:
        if m not in list('BVRJHK'):
            raise ValueError('Magnitude band %s not available in NOMAD1 catalog' % m)
        min, max = mag[m]
        args.append('-lc%s' % m)
        args.append('%f,%f' % (min, max))

    result = subprocess.check_output(args)
    result = result.decode('ascii', errors='ignore')

    stars = []
    for line in result.split('\n'):
        if len(line) < 1 or line[0] == '#':
            continue

        _, _, coords, _, _, bvr, jhk, R, _ = line.split('|')
        Bmag, Vmag, Rmag = bvr.split()
        Jmag, Hmag, Kmag = jhk.split()

        radec = coords.split()[0]
        Bmag = _convert_mag(Bmag)
        Vmag = _convert_mag(Vmag)
        Rmag = _convert_mag(Rmag)
        Jmag = _convert_mag(Jmag)
        Hmag = _convert_mag(Hmag)
        Kmag = _convert_mag(Kmag)
        R = R.strip()
        if R:
            print('R:', R)
            R = float(R) 
        else:
            R = None

        stars.append(NOMAD1Star(radec, Bmag, Vmag, Rmag, Jmag, Hmag, Kmag,R))

    return stars

