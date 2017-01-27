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
import sys

import numpy


def load_npz(file_name):
    """
    This function tries to load a numpy ``*.npz`` file.

    If the file's name contains ``built-in `` at the start, it will attempt to load the file
    from the ``package_data`` as specified in the ``setup.py`` install script for this module.

    Otherwise it tries to load the file as usual.

    The NPZ file is expected to contain a single keyword, the data associated with that keyword is returned.

    :param file_name: A file name or file object to read data from
    :type file_name: :py:class:`file` or :py:class:`str`
    :rtype: :py:class:`numpy.ndarray`
    """

    # noinspection PyUnresolvedReferences
    loader_input = \
        io.BytesIO(pkgutil.get_data('httm', os.path.join('/data', re.match(r'^built-in (.*)', file_name).group(1)))) \
        if (isinstance(file_name, str) or (sys.version_info <= (3, 0) and isinstance(file_name, unicode))) and \
           ((not os.path.isfile(file_name)) and re.match(r'^built-in (.*)', file_name)) \
        else file_name

    data = numpy.load(loader_input)

    keys = tuple(data.keys())
    assert len(keys) == 1, "Loaded NPZ data can only have one entry"

    return data[keys[0]]
