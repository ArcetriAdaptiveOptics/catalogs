#!/usr/bin/env python

import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='catalogs',
    version='0.1.0',
    author='Alfio Puglisi',
    author_email='alfio.puglisi@inaf.it',
    description='Python wrapper for all-sky catalogs',
    long_description=long_description,
    url='https://github.com/ArcetriAdaptiveOptics/catalogs',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    packages=['catalogs'],
)
