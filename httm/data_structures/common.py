# HTTM: A transformation library for RAW and Electron Flux TESS Images
# Copyright (C) 2016, 2017 John Doty and Matthew Wampler-Doty of Noqsi Aerospace, Ltd.
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""
``httm.data_structures.common``
===============================

Common data structures used in transformations of FITS images.
"""

from collections import namedtuple


# noinspection PyUnresolvedReferences,PyClassHasNoInit
class ConversionMetaData(
    namedtuple('ConversionMetaData', ['origin_file_name', 'command', 'header'])):
    """
    Meta data associated with data taken from a FITS file.

    :param origin_file_name: The original file name where the data was taken from
    :type origin_file_name: str
    :param header: The header of the FITS file where the data was taken from
    :type header: :py:class:`astropy.io.fits.Header`
    """
    __slots__ = ()


# noinspection PyUnresolvedReferences,PyClassHasNoInit
class Slice(
    namedtuple('Slice', ['index', 'units', 'pixels'])):
    """
    A slice from a CCD. Includes all data associated with the slice in question
    from various parts of the raw CCD image.


    :param index: The index of the slice in the CCD
    :param units: Can be either `electrons` or `ADU`
    :type units: str
    :param pixels: The slice image data
    :type pixels: :py:class:`numpy.ndarray`
    """
    __slots__ = ()
