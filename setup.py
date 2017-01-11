#!/usr/bin/env python

from setuptools import setup, find_packages
from glob import glob

VERSION = '0.1.2'

setup(
    name='httm',
    version=VERSION,
    description='A transformation library for RAW and Electron Flux TESS Images',
    author='Matthew Wampler-Doty, John Doty',
    author_email='matthew.wampler.doty@gmail.com, jpd@noqsi.com',
    packages=find_packages('.'),
    package_data={'httm': ['data/*.npz']},
    install_requires=['numpy', 'astropy>=1.3', 'toml', 'pyyaml', 'xmltodict'],
    scripts=glob('scripts/*'),
)
