"""
``httm.fits_utilities.raw_fits``
================================

This module contains functions for marshalling and de-marshalling
:py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter` and the other book-keeping objects
it contains to and from FITS files or :py:class:`astropy.io.fits.HDUList` objects.
"""

import os

import astropy
import numpy
from astropy.io.fits import HDUList, PrimaryHDU

from .header_settings import get_header_setting
from ..data_structures.common import Slice, FITSMetaData
from ..data_structures.raw_converter import SingleCCDRawConverterFlags, SingleCCDRawConverter, \
    raw_transformation_flags, SingleCCDRawConverterParameters, raw_converter_parameters


# TODO: Documentation
# noinspection PyUnresolvedReferences
def raw_converter_to_calibrated_hdulist(converter):
    # type: (SingleCCDRawConverter) -> HDUList
    """
    TODO: Document me

    :param converter:
    :rtype: NoneType
    """
    # noinspection PyTypeChecker
    early_dark_pixel_columns = converter.parameters.early_dark_pixel_columns  # type: int
    late_dark_pixel_columns = converter.parameters.late_dark_pixel_columns  # type: int
    left_dark_parts = [raw_slice.pixels[:, :early_dark_pixel_columns]
                       for raw_slice in converter.slices]  # type: list
    right_dark_parts = [raw_slice.pixels[:, -late_dark_pixel_columns:]
                        for raw_slice in converter.slices]  # type: list
    image_parts = [raw_slice.pixels[:, early_dark_pixel_columns:-late_dark_pixel_columns]
                   for raw_slice in converter.slices]  # type: list

    for i in range(1, len(converter.slices), 2):
        left_dark_parts[i] = numpy.fliplr(left_dark_parts[i])
        right_dark_parts[i] = numpy.fliplr(right_dark_parts[i])
        image_parts[i] = numpy.fliplr(image_parts[i])

    # TODO: Write parameters and flags to HDU header
    return HDUList(PrimaryHDU(header=converter.fits_metadata.header,
                              # `+` concatenates python lists
                              data=numpy.hstack(left_dark_parts + image_parts + right_dark_parts)))


# TODO: Documentation
def write_raw_converter_to_calibrated_fits(converter, output_file):
    # type: (SingleCCDRawConverter, str) -> None
    """
    Write a completed :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter`
    to a calibrated FITS file

    :param converter:
    :type converter: :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter`
    :param output_file:
    :type output_file: :py:class:`file` or :py:class:`str`
    :rtype: NoneType
    """
    hdulist = raw_converter_to_calibrated_hdulist(converter)

    try:
        os.remove(output_file)
    except OSError:
        pass

    hdulist.writeto(output_file)


# TODO: Documentation
def raw_converter_flags_from_fits_header(fits_header, flag_overrides=None):
    """
    Construct a :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverterFlags`
    from a FITS header.

    TODO: Document me

    :param fits_header: FITS header to use for parsing parameters
    :type fits_header: :py:class:`astropy.io.fits.Header`
    :param flag_overrides:
    :type flag_overrides: object
    :rtype: :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverterFlags`
    """

    def get_flag(flag_name):
        return get_header_setting(
            flag_name,
            raw_transformation_flags,
            fits_header,
            getattr(flag_overrides, flag_name) if hasattr(flag_overrides, flag_name) else None)

    return SingleCCDRawConverterFlags(
        smear_rows_present=get_flag('smear_rows_present'),
        undershoot_present=get_flag('undershoot_present'),
        pattern_noise_present=get_flag('pattern_noise_present'),
        start_of_line_ringing_present=get_flag('start_of_line_ringing_present'),
        baseline_present=get_flag('baseline_present'),
        in_adu=get_flag('in_adu'),
    )


# TODO: Documentation
def raw_converter_parameters_from_fits_header(fits_header, parameter_overrides=None):
    """
    TODO: Document this

    :param fits_header: FITS header to use for parsing parameters
    :type fits_header: :py:class:`astropy.io.fits.Header`
    :param parameter_overrides:
    :type parameter_overrides: object
    :return:
    """

    def get_parameter(parameter_name):
        return get_header_setting(
            parameter_name,
            raw_converter_parameters,
            fits_header,
            getattr(parameter_overrides, parameter_name) if hasattr(parameter_overrides, parameter_name) else None)

    return SingleCCDRawConverterParameters(
        number_of_slices=get_parameter('number_of_slices'),
        camera_number=get_parameter('camera_number'),
        ccd_number=get_parameter('ccd_number'),
        number_of_exposures=get_parameter('number_of_exposures'),
        video_scales=get_parameter('video_scales'),
        early_dark_pixel_columns=get_parameter('early_dark_pixel_columns'),
        late_dark_pixel_columns=get_parameter('late_dark_pixel_columns'),
        final_dark_pixel_rows=get_parameter('final_dark_pixel_rows'),
        smear_rows=get_parameter('smear_rows'),
        gain_loss=get_parameter('gain_loss'),
        undershoot_parameter=get_parameter('undershoot_parameter'),
        pattern_noise=get_parameter('pattern_noise'),
    )


def make_slice_from_raw_data(
        image_and_smear_pixels,
        index,
        early_dark_pixel_columns,
        late_dark_pixel_columns):
    # type: (numpy.ndarray, int, numpy.ndarray, numpy.ndarray) -> Slice
    """
    Construct a slice from raw pixel data given a specified index.

    Result is in *Analogue to Digital Converter Units* (ADU).

    :param image_and_smear_pixels: Image pixels from the raw FITS data.
    :type image_and_smear_pixels: :py:class:`numpy.ndarray`
    :param index: The index of the slice to construct.
    :type index: int
    :param early_dark_pixel_columns: The leftmost columns are dark pixels, to be placed on the \
    left of the slice.
    :type early_dark_pixel_columns: :py:class:`numpy.ndarray`
    :param late_dark_pixel_columns: The rightmost columns are dark pixels, to be placed on the \
    right of the slice.
    :type late_dark_pixel_columns: :py:class:`numpy.ndarray`
    :rtype: :py:class:`~httm.data_structures.common.Slice`
    """
    return Slice(
        pixels=numpy.hstack([early_dark_pixel_columns, image_and_smear_pixels, late_dark_pixel_columns]),
        index=index,
        units='ADU')


# TODO Documentation
# noinspection PyUnresolvedReferences
def raw_converter_from_hdulist(header_data_unit_list,
                               origin_file_name=None,
                               flag_overrides=None,
                               parameter_overrides=None):
    """
    TODO: Document this

    :param header_data_unit_list:
    :param origin_file_name:
    :param flag_overrides:
    :param parameter_overrides:
    :rtype: SingleCCDRawConverter
    """
    from numpy import hsplit, fliplr
    fits_metadata = FITSMetaData(origin_file_name=origin_file_name,
                                 header=header_data_unit_list[0].header)  # type: FITSMetaData
    flag_overrides = raw_converter_flags_from_fits_header(fits_metadata, flag_overrides=flag_overrides)
    parameter_overrides = raw_converter_parameters_from_fits_header(fits_metadata,
                                                                    parameter_overrides=parameter_overrides)
    assert len(header_data_unit_list) == 1, "Only a single image per FITS file is supported"
    assert header_data_unit_list[0].data.shape[1] % parameter_overrides.number_of_slices == 0, \
        "Image did not have the specified number of slices"

    early_dark_pixel_count = parameter_overrides.number_of_slices * parameter_overrides.early_dark_pixel_columns
    late_dark_pixel_count = parameter_overrides.number_of_slices * parameter_overrides.late_dark_pixel_columns
    sliced_image_smear_and_dark_pixels = hsplit(
        header_data_unit_list[0].data[:, early_dark_pixel_count:-late_dark_pixel_count],
        parameter_overrides.number_of_slices)

    # TODO: Document this in layout.rst
    # Rows in odd numbered slices have to be reversed
    for i in range(1, parameter_overrides.number_of_slices, 2):
        sliced_image_smear_and_dark_pixels[i] = fliplr(sliced_image_smear_and_dark_pixels[i])

    # Note that left and right dark pixels do not need to be reversed
    sliced_early_dark_pixels = hsplit(header_data_unit_list[0].data[:, :early_dark_pixel_count],
                                      parameter_overrides.number_of_slices)
    sliced_late_dark_pixels = hsplit(header_data_unit_list[0].data[:, -late_dark_pixel_count:],
                                     parameter_overrides.number_of_slices)

    return SingleCCDRawConverter(
        slices=tuple(map(make_slice_from_raw_data,
                         sliced_image_smear_and_dark_pixels,
                         range(parameter_overrides.number_of_slices),
                         sliced_early_dark_pixels,
                         sliced_late_dark_pixels)),
        fits_metadata=fits_metadata,
        parameters=parameter_overrides,
        flags=flag_overrides,
    )


# TODO: Documentation
def raw_converter_from_fits(input_file, flag_overrides=None, parameter_overrides=None):
    """
    TODO: Document this

    :param input_file:
    :param flag_overrides:
    :param parameter_overrides:
    :rtype:
    """
    return raw_converter_from_hdulist(
        astropy.io.fits.open(input_file),
        origin_file_name=input_file,
        flag_overrides=flag_overrides,
        parameter_overrides=parameter_overrides,
    )
