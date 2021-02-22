#!/usr/bin/env python
'''
Module to query a local copy of the GSC2.3 catalog

A. Puglisi, Feb 2021
'''

import subprocess
from collections import namedtuple

from catalog_conf import gsc23_exe, gsc23_dir


GSC23Star = namedtuple('GSC23Star', 'radec fmag jmag vmag nmag umag bmag R')

def _convert_mag(mag_str):
    if '---' in mag_str:
        return None
    return float(mag_str.split()[0])   


def query(ra, dec, radius_arcsec, catalog_dir=None, exefile=None, max=None, mag={}):
    '''Query the GSC23 catalog

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
        directory with GSC23 data files
    exefile: string, optional
        GSC23 search program
    '''
    exefile = exefile or gsc23_exe
    catalog_dir = catalog_dir or gsc23_dir
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
        if m not in list('JVFNUB'):
            raise ValueError('Magnitude band %s not available in GSC catalog' % m)
        min, max = mag[m]
        args.append('-l%s' % m)
        args.append('%f,%f' % (min, max))

    result = subprocess.check_output(args)
    result = result.decode('ascii', errors='ignore')

    stars = []
    for line in result.split('\n'):
        if len(line) < 1 or line[0] == '#':
            continue
        num, coords, Fmag, Jmag, Vmag, Nmag, Umag, Bmag, Cl, Size, R = line.split('|')

        radec = coords.split()[0]
        Fmag = _convert_mag(Fmag)
        Jmag = _convert_mag(Jmag)
        Vmag = _convert_mag(Vmag)
        Nmag = _convert_mag(Nmag)
        Umag = _convert_mag(Umag)
        Bmag = _convert_mag(Bmag)
        R = float(R[1:]) 

        stars.append(GSC23Star(radec, Fmag, Jmag, Vmag, Nmag, Umag, Bmag, R))

    return stars

