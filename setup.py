#!/usr/bin/env python

from setuptools import setup

VERSION = '0.1.0'

setup(name='httm',
      version=VERSION,
      description='A transformation library for RAW and Calibrated TESS Images',
      author='Matthew Wampler-Doty',
      author_email='matthew.wampler.doty@gmail.com',
      packages=['httm'],
      install_requires=['numpy', 'astropy==1.1.2']
      )
