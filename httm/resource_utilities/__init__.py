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

import numpy
from numpy import ndarray


def get_file_resource(file_name):
    match = re.match(r'^built-in (.*)', file_name)
    # Note: This CANNOT handle GZIPed FITS files in package_data
    return io.BytesIO(pkgutil.get_data('httm', os.path.join('/data', match.group(1)))) \
        if ((not os.path.isfile(file_name)) and match) else file_name


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

    data = numpy.load(get_file_resource(npz_file_name))

    keys = tuple(data.keys())
    assert len(keys) == 1, "Loaded NPZ data can only have one entry"

    return data[keys[0]]


# TODO: Documentation
def load_pattern_noise(file_name):
    from .. import fits_utilities
    slices = fits_utilities.raw_converter_from_fits(get_file_resource(file_name)).slices
    return tuple(s.pixels for s in slices)
