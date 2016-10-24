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

CalibratedTransformParameters = namedtuple('CalibratedTransformParameters',
                                           default_calibrated_transform_parameters.keys())
CalibratedTransformParameters.__new__.__defaults__ = tuple(default_calibrated_transform_parameters.values())

RAWTransformParameters = namedtuple('RAWTransformParameters', default_raw_transform_parameters.keys())
RAWTransformParameters.__new__.__defaults__ = tuple(default_raw_transform_parameters.values())

FITSMetaData = namedtuple(
    'FITSMetaData',
    ['origin_file_name',
     'header'])

Slice = namedtuple(
    'Slice',
    ['smear_rows',
     'top_dark_pixels_rows',
     'left_dark_pixels_columns',
     'right_dark_pixels_columns',
     'index',
     'units',
     'image_pixels'])
Slice.__new__.__defaults__ = (None,) * len(Slice._fields)

RAWTransformation = namedtuple(
    'RAWTransformation',
    ['slices',
     'fits_metadata',
     'parameters'])

CalibratedTransformation = namedtuple(
    'CalibratedTransformation',
    ['slices',
     'fits_metadata',
     'parameters'])


def write_calibrated_fits(output_file, raw_transform):
    from astropy.io.fits import HDUList, PrimaryHDU
    from numpy import hstack
    print raw_transform
    # noinspection PyTypeChecker
    HDUList(PrimaryHDU(header=raw_transform.fits_metadata.header,
                       data=hstack([calibrated_slice.image_pixels
                                    for calibrated_slice in raw_transform.slices]))) \
        .writeto(output_file)


def write_raw_fits(output_file, calibrated_transform):
    from astropy.io.fits import HDUList, PrimaryHDU
    from numpy import hstack
    # noinspection PyTypeChecker
    HDUList(PrimaryHDU(header=calibrated_transform.fits_metadata.header,
                       data=hstack([raw_slice.image_pixels
                                    for raw_slice in calibrated_transform.slices]))) \
        .writeto(output_file)


def make_slice_from_calibrated_data(image_pixels, index):
    """Construct a slice from an array of calibrated pixel data and a specified index"""
    return Slice(image_pixels=image_pixels,
                 index=index,
                 units='electrons')


def calibrated_transform_from_file(input_file, number_of_slices=4, **kwargs):
    """Construct a CalibratedTransformation from a file or file name"""
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
    """Construct a RAWTransformation from a file or file name"""
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
    make_raw_pixel_slice = lambda image_pixels, index, left_dark_pixels_columns, right_dark_pixels_columns, top_dark_pixels_rows, smear_rows: Slice(
        image_pixels=image_pixels,
        index=index,
        left_dark_pixels_columns=left_dark_pixels_columns,
        right_dark_pixels_columns=right_dark_pixels_columns,
        top_dark_pixels_rows=top_dark_pixels_rows,
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
