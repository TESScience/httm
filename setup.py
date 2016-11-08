#!/usr/bin/env python

from setuptools import setup, find_packages
from glob import glob

VERSION = '0.1.0'

setup(
    name='httm',
    version=VERSION,
    description='A transformation library for RAW and Calibrated TESS Images',
    author='Matthew Wampler-Doty, John Doty',
    author_email='matthew.wampler.doty@gmail.com, jpd@noqsi.com',
    packages=find_packages('.'),
    install_requires=['numpy', 'astropy==1.1.2'],
    scripts=glob('scripts/*'),
)
