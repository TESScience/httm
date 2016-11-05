"""
``httm.data_structures.common``
===============================

Common data structures used in transformations of FITS images.
"""

from collections import namedtuple


# noinspection PyUnresolvedReferences,PyClassHasNoInit
class FITSMetaData(
    namedtuple('FITSMetaData',
               ['origin_file_name', 'header'])):
    """
    Meta data associated with data taken from a FITS file.

    :param origin_file_name: The original file name where the data was taken from
    :type origin_file_name: str
    :param header: The header of the FITS file where the data was taken from
    :type header: :py:class:`pyfits.Header`
    """
    __slots__ = ()


# noinspection PyUnresolvedReferences,PyClassHasNoInit
class Slice(
    namedtuple('Slice',
               ['index',
                'units',
                'pixels'])):
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
