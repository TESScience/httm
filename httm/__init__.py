# See https://docs.python.org/2/library/collections.html#collections.namedtuple for details
from collections import namedtuple

import numpy

default_calibrated_transform_parameters = {
    'video_scale': (5.5, 5.5, 5.5, 5.5),  # electrons/ADU
    'number_of_slices': 4,  # number of slices to use in transformation, either 1 or 4
    'compression': 0.01,
    'undershoot': 0.001,
    'baseline_adu': 6000.0,
    'drift_adu': 10.0,
    'smear_ratio': 9.79541e-6,  # Derived from Hemiola.fpe
    'clip_level_adu': 60000,
    'start_of_line_ringing': numpy.zeros(534),  # TODO: Read this from a file
    'pattern_noise': numpy.zeros((2078, 534))  # TODO: Read this from a file
}

default_raw_transform_parameters = {
    k: default_calibrated_transform_parameters[k]
    for k in [
        'video_scale',
        'number_of_slices',
        'compression',
        'undershoot',
        'smear_ratio',
        'clip_level_adu',
        'pattern_noise'
    ]}


# noinspection PyUnresolvedReferences
class CalibratedTransformParameters(
    namedtuple('CalibratedTransformParameters',
               default_calibrated_transform_parameters.keys())):
    __doc__ = """
    Transformation parameters for converting a calibrated FITS image into an uncalibrated FITS image.

    :param video_scale: The video scaling constants. Default: `{video_scale}`
    :type video_scale: tuple of :py:class:`float` objects, must have one for each slice
    :param number_of_slices: The number of slices to make in the resulting uncalibrated image. Default: `{number_of_slices}`
    :type number_of_slices: int
    :param compression: The compression factor. Default: `{compression}`
    :type compression: float
    :param undershoot: The undershoot factor. Default: `{undershoot}`
    :type undershoot: float
    :param baseline_adu: The baseline adu factor. Default: `{baseline_adu}`
    :type baseline_adu: float
    :param drift_adu: The drift ADU factor. Default: `{drift_adu}`
    :type drift_adu: float
    :param smear_ratio: The smear ratio. Default: `{smear_ratio}`
    :type smear_ratio: float
    :param clip_level_adu: The clip level ADU. Default: `{clip_level_adu}`
    :type clip_level_adu: int
    :param start_of_line_ringing: The start of line ringing vector. Default: Read from **TODO**
    :type start_of_line_ringing: :py:class:`numpy.ndarray`
    :param pattern_noise: The pattern noise. Default: Read from **TODO**
    :type pattern_noise: :py:class:`numpy.ndarray`
    """.format(**default_calibrated_transform_parameters)
    __slots__ = ()


CalibratedTransformParameters.__new__.__defaults__ = tuple(default_calibrated_transform_parameters.values())


# noinspection PyUnresolvedReferences
class RAWTransformParameters(
    namedtuple('RAWTransformParameters',
               default_raw_transform_parameters.keys())):
    """
    Transformation parameters for converting a calibrated FITS image into an uncalibrated FITS image.

    :param video_scale:
    :param number_of_slices:
    :param compression:
    :param undershoot:
    :param smear_ratio:
    :param clip_level_adu:
    :param pattern_noise:
    """
    __slots__ = ()


RAWTransformParameters.__new__.__defaults__ = tuple(default_raw_transform_parameters.values())


# noinspection PyUnresolvedReferences
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


# noinspection PyUnresolvedReferences
class Slice(namedtuple('Slice',
                       ['smear_rows',
                        'top_dark_pixel_rows',
                        'left_dark_pixel_columns',
                        'right_dark_pixel_columns',
                        'index',
                        'units',
                        'image_pixels'])):
    __doc__ = """
    A slice from a CCD. Includes all data associated with the slice in question
    from various parts of the raw CCD image.

    :param smear_rows:
    :param top_dark_pixel_rows:
    :param left_dark_pixel_columns:
    :param right_dark_pixel_columns:
    :param index: The index of the slice in the CCD
    :param units:
    :param image_pixels: The image data in the pixel
    """
    __slots__ = ()


Slice.__new__.__defaults__ = (None,) * len(Slice._fields)


# noinspection PyUnresolvedReferences
class RAWTransformation(namedtuple('RAWTransformation',
                                   ['slices',
                                    'fits_metadata',
                                    'parameters'])):
    """
    An object for managing a transformation from a raw FITS image into a calibrated image.

    :param slices: The slices of the image
    :type slices: list of :py:class:`~httm.Slice` objects
    :param fits_metadata: Meta data associated with the image
    :type fits_metadata: :py:class:`~httm.FITSMetaData`
    :param parameters: The parameters of the transformation
    :type parameters: :py:class:`~httm.RAWTransformParameters`
    """
    __slots__ = ()


# noinspection PyUnresolvedReferences
class CalibratedTransformation(namedtuple('CalibratedTransformation',
                                          ['slices',
                                           'fits_metadata',
                                           'parameters'])):
    """
    An object for managing a transformation from a calibrated FITS image into a (simulated) raw image.

    :param slices: The slices of the image
    :type slices: list[:py:class:`~httm.Slice`]
    :param fits_metadata: Meta data associated with the image
    :type fits_metadata: :py:class:`~httm.FITSMetaData`
    :param parameters: The parameters of the transformation
    :type parameters: :py:class:`~httm.CalibratedTransformParameters`
    """


def write_calibrated_fits(output_file, raw_transform):
    """
    Write a completed :py:class:`~httm.RAWTransformation` to a calibrated FITS file

    :param output_file:
    :type output_file: str
    :param raw_transform:
    :type raw_transform: :py:class:`~httm.RAWTransformation`
    :return: NoneType
    """
    from astropy.io.fits import HDUList, PrimaryHDU
    from numpy import hstack
    print raw_transform
    # noinspection PyTypeChecker
    HDUList(PrimaryHDU(header=raw_transform.fits_metadata.header,
                       data=hstack([calibrated_slice.image_pixels
                                    for calibrated_slice in raw_transform.slices]))) \
        .writeto(output_file)


def write_raw_fits(output_file, calibrated_transform):
    """
    Write a completed :py:class:`~httm.CalibratedTransformation` to a (simulated) raw FITS file

    :param output_file:
    :type output_file: str
    :param calibrated_transform:
    :type calibrated_transform: :py:class:`~httm.CalibratedTransformation`
    :return: NoneType
    """
    from astropy.io.fits import HDUList, PrimaryHDU
    from numpy import hstack
    # noinspection PyTypeChecker
    HDUList(PrimaryHDU(header=calibrated_transform.fits_metadata.header,
                       data=hstack([raw_slice.image_pixels
                                    for raw_slice in calibrated_transform.slices]))) \
        .writeto(output_file)


def make_slice_from_calibrated_data(image_pixels, index):
    """
    Construct a slice from an array of calibrated pixel data given a specified index

    :param image_pixels: Image pixels from the calibrated data
    :type image_pixels: :py:class:`numpy.ndarray`
    :param index: The index of the slice to construct
    :type index: int
    :rtype: :py:class:`~httm.Slice`
    """
    return Slice(image_pixels=image_pixels,
                 index=index,
                 units='electrons')


def calibrated_transform_from_file(input_file, number_of_slices=4, **kwargs):
    """
    Construct a :py:class:`~httm.CalibratedTransformation` from a file or file name

    :param input_file: The file or file name to input
    :param number_of_slices: The numbers of slices
    :type input_file: :py:class:`File` or :py:class:`str`
    :rtype: :py:class:`~httm.CalibratedTransformation`
    """
    from astropy.io import fits
    from numpy import hsplit
    header_data_unit_list = fits.open(input_file)
    assert len(header_data_unit_list) == 1, "Only a single image per FITS file is supported"
    assert header_data_unit_list[0].data.shape[1] % number_of_slices == 0, \
        "Image did not have the specified number of slices"
    origin_file_name = None
    if isinstance(input_file, basestring):
        origin_file_name = input_file
    if hasattr(input_file, 'name'):
        origin_file_name = input_file.name
    return CalibratedTransformation(
        slices=map(lambda pixel_data, index:
                   make_slice_from_calibrated_data(pixel_data, index),
                   hsplit(header_data_unit_list[0].data, number_of_slices),
                   range(number_of_slices)),
        fits_metadata=FITSMetaData(origin_file_name=origin_file_name,
                                   header=header_data_unit_list[0].header),
        parameters=CalibratedTransformParameters(number_of_slices=number_of_slices, **kwargs))


def raw_transform_from_file(input_file, number_of_slices=4, **kwargs):
    """
    Construct a :py:class:`~httm.RAWTransformation` from a file or file name

    :param input_file: The file or file name to input
    :type input_file: :py:class:`File` or :py:class:`str`
    :rtype: :py:class:`~httm.RAWTransformation`
    """
    from astropy.io import fits
    from numpy import hsplit, vsplit
    header_data_unit_list = fits.open(input_file)
    assert len(header_data_unit_list) == 1, "Only a single image per FITS file is supported"
    assert header_data_unit_list[0].data.shape[1] % number_of_slices == 0, \
        "Image did not have the specified number of slices"
    origin_file_name = None
    if isinstance(input_file, basestring):
        origin_file_name = input_file
    if hasattr(input_file, 'name'):
        origin_file_name = input_file.name

    sliced_image_pixels = hsplit(header_data_unit_list[0].data[20:, 44:-44], number_of_slices)
    sliced_left_dark_pixels = vsplit(header_data_unit_list[0].data[:, :44], number_of_slices)
    sliced_right_dark_pixels = vsplit(header_data_unit_list[0].data[:, -44:], number_of_slices)
    sliced_top_dark_pixels = hsplit(header_data_unit_list[0].data[:10, 44:-44], number_of_slices)
    sliced_smear_rows = hsplit(header_data_unit_list[0].data[10:20, 44:-44], number_of_slices)
    # TODO: Factor me out
    make_raw_pixel_slice = lambda image_pixels, index, left_dark_pixel_columns, right_dark_pixel_columns, \
                                  top_dark_pixel_rows, smear_rows: Slice(
        image_pixels=image_pixels,
        index=index,
        left_dark_pixel_columns=left_dark_pixel_columns,
        right_dark_pixel_columns=right_dark_pixel_columns,
        top_dark_pixel_rows=top_dark_pixel_rows,
        smear_rows=smear_rows,
        units='hdu')
    return RAWTransformation(
        slices=map(make_raw_pixel_slice,
                   sliced_image_pixels,
                   range(number_of_slices),
                   sliced_left_dark_pixels,
                   sliced_right_dark_pixels,
                   sliced_top_dark_pixels,
                   sliced_smear_rows),
        fits_metadata=FITSMetaData(origin_file_name=origin_file_name,
                                   header=header_data_unit_list[0].header),
        parameters=RAWTransformParameters(number_of_slices=number_of_slices, **kwargs))
