#!/usr/bin/env python
#
# Make a test image of four 50 x 50 slices for blooming and undershoot
# This puts 1000000 (implicitly electrons) in pixel [25, 25]. The rest of the image is 100.
import numpy
image_data=numpy.zeros((50,200))+100
image_data[25,25]=1000000
from astropy.io import fits
fits.writeto('spot50.fits', image_data, None, clobber=True)
