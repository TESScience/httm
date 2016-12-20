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

    if isinstance(file_name, str) and not os.path.isfile(file_name):
        pattern_match = re.match(r'^built-in (.*)', file_name)
        if pattern_match:
            return numpy.load(io.BytesIO(pkgutil.get_data(
                'httm', os.path.join('/data', pattern_match.group(1)))))[resource_key]

    return numpy.load(file_name)[resource_key]
