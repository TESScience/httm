#!/usr/bin/env python
#
# Make a 50 x 50 test image for blooming and undershoot
# This puts 1000000 (implicitly electrons) in pixel [25, 25]. The rest of the image is zero.
import numpy
image_data=numpy.zeros((50,50))
image_data[25,25]=1000000
from astropy.io import fits
fits.writeto('spot50.fits', image_data, None, clobber=True)
