HTTM
====

[![Documentation Status](http://readthedocs.org/projects/httm/badge/?version=latest)](https://httm.readthedocs.io/en/latest/)
[![Build Status](https://travis-ci.org/TESScience/httm.svg?branch=master)](https://travis-ci.org/TESScience/httm)

This repository contains `httm`, a library for converting between raw *Transiting Exoplanet Survey Satellite* (TESS) FITS images to calibrated FITS images and back.

A raw TESS FITS image is an image taken by either the space craft or the CCD testing systems used prior to launch, and measured in *Analogue To Digital Converter Units* (ADU).

Calibrated FITS images are converted from raw FITS images, or created synthetically by tools like [SPyFFI](https://github.com/TESScience/SPyFFI).  They have electrons as units rather than ADU and try to compensate for systematic errors introduced by the electronics.

## Installing HTTM

To install `httm`, type at the command line:

    pip install git+https://github.com/TESScience/httm.git

## Documentation

See the [**Official Online Documentation**](https://httm.readthedocs.io/)

## Development

See the [**Development Documentation**](DEVELOPMENT.md "Development")

## Licensing

Copyright (C) 2016, 2017 John Doty and Matthew Wampler-Doty of Noqsi Aerospace, Ltd.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

## Support

Please file bugs and issues on the Github issues page for this project.
