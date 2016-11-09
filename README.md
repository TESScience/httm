HTTM
====

[![Documentation Status](http://readthedocs.org/projects/httm/badge/?version=latest)](https://httm.readthedocs.io/en/latest/)

This repository contains `httm`, a library for converting between raw *Transiting Exoplanet Survey Satellite* (TESS) FITS images to calibrated FITS images and back.

A raw TESS FITS image is an image taken by either the space craft or the CCD testing systems used prior to launch, and measured in *Analogue To Digital Converter Units* (ADU).

Calibrated FITS images are converted from raw FITS images, or created synthetically by tools like [SPyFFI](https://github.com/TESScience/SPyFFI).  They have electrons as units rather than ADU and try to compensate for systematic errors introduced by the electronics.

## Installing HTTM

To install `httm`, type at the command line:

    pip install httm

## Documentation

[**Official Online Documentation**](https://httm.readthedocs.io/)

To build the documentation, execute the following command at the command line in the directory this file is contained:

    make documentation

You will need [pandoc](http://pandoc.org/ "Pandoc"), [jupyter](https://jupyter.org/ "Jupyter") and [sphinx](http://www.sphinx-doc.org/ "Sphinx"]) installed. If this is successful, you can view a PDF of the documentation in the directory:
    
    ./doc/build/latex/HTTM.pdf

## Running Tests

To run the unit tests for this software, execute the following command at the command line in the directory this file is contained:

    make test

## Licensing

HTTM is licensed under the  [MIT](http://opensource.org/licenses/MIT "The MIT License (MIT)") license: 

The MIT License (MIT)

Copyright (c) 2016, NoqsiAerospace, Ltd.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


## Support

Please file bugs and issues on the Github issues page for this project.