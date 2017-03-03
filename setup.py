#!/usr/bin/env python

from glob import glob

from setuptools import setup, find_packages

VERSION = '0.2.2'

setup(
    name='httm',
    version=VERSION,
    description='A transformation library for RAW and Electron Flux TESS Images',
    author='Matthew Wampler-Doty, John Doty',
    author_email='matthew.wampler.doty@gmail.com, jpd@noqsi.com',
    url='https://github.com/TESScience/httm',
    download_url='https://github.com/TESScience/httm/tarball/{VERSION}'.format(VERSION=VERSION),
    packages=find_packages('.'),
    package_data={'httm': ['data/*.npz', 'data/*.fits']},
    install_requires=['numpy', 'astropy>=1.3', 'toml'],
    scripts=glob('scripts/*'),
)
