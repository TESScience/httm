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
``httm.resource_utilities``
===========================

This module contains functions for dealing with package data.
"""

import io
import os
import pkgutil
import re

import astropy.io.fits
import numpy
from numpy import ndarray


# TODO: Documentation
def load_fits_image_data(fits_file_name, checksum=True):
    # type: (str) -> ndarray
    """
    This function tries to load data from a FITS image.

    :param fits_file_name:
    :type fits_file_name: :py:class:`str`
    :param checksum:
    :type checksum: bool
    :rtype: :py:class:`numpy.ndarray`
    """
    return astropy.io.fits.open(fits_file_name, checksum=checksum)[0].data


# noinspection SpellCheckingInspection
def load_npz(npz_file_name):
    # type: (str) -> ndarray
    """
    This function tries to load a numpy ``*.npz`` file.

    If the file's name contains the string ``"built-in "`` at the start, it will attempt to load the file
    from the ``package_data`` directory as specified in the ``setup.py`` install script for this module.

    Otherwise it tries to load the file as usual.

    The NPZ file is expected to contain a single keyword, the data associated with that keyword is returned.

    :param npz_file_name: A file name or file object to read data from
    :type npz_file_name: :py:class:`str`
    :rtype: :py:class:`numpy.ndarray`
    """

    # noinspection PyUnresolvedReferences
    loader_input = \
        io.BytesIO(pkgutil.get_data('httm', os.path.join('/data',
                                                         re.match(r'^built-in (.*)', npz_file_name).group(1)))) \
        if ((not os.path.isfile(npz_file_name)) and re.match(r'^built-in (.*)', npz_file_name)) else npz_file_name

    data = numpy.load(loader_input)

    keys = tuple(data.keys())
    assert len(keys) == 1, "Loaded NPZ data can only have one entry"

    return data[keys[0]]


# TODO: Documentation
def load_data(file_name):
    if re.match(r'.*\.npz$', file_name):
        return load_npz(file_name)
    elif re.match(r'.*\.fits.*$', file_name):
        return load_fits_image_data(file_name)
    else:
        raise Exception("File has unknown suffix: {}".format(file_name))
