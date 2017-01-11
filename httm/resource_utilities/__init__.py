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


def load_npz_resource(file_name, resource_key):
    """
    This function tries to load a numpy ``*.npz`` file.

    If the file's name contains ``:httm:`` at the start, it will attempt to load the file
    from `httm`'s ``package_data`` as specified in ``setup.py``.

    Otherwise it tries to load the file as usual.

    :param file_name: A file name or file object to read data from
    :type file_name: :py:class:`file` or :py:class:`str`
    :param resource_key: The key name of the desired data resource contained in the ``*.npz`` file.
    :type resource_key: :py:class:`str`
    :rtype: :py:class:`numpy.ndarray`
    """

    if isinstance(file_name, str) or isinstance(file_name, unicode) and not os.path.isfile(file_name):
        pattern_match = re.match(r'^built-in (.*)', file_name)
        if pattern_match:
            return numpy.load(io.BytesIO(pkgutil.get_data(
                'httm', os.path.join('/data', pattern_match.group(1)))))[resource_key]

    return numpy.load(file_name)[resource_key]
