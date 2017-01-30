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
``httm.fits_utilities.raw_fits``
================================

This module contains functions for marshalling and de-marshalling
:py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter` and the other book-keeping objects
it contains to and from FITS files or :py:class:`astropy.io.fits.HDUList` objects.
"""

import os
from collections import namedtuple

import astropy
import numpy
from astropy.io.fits import HDUList, PrimaryHDU

from .header_tools import get_header_setting, set_header_settings, add_command_to_header_history
from ..data_structures.common import Slice, ConversionMetaData
from ..data_structures.raw_converter import SingleCCDRawConverterFlags, SingleCCDRawConverter, \
    raw_transformation_flags, SingleCCDRawConverterParameters, raw_converter_parameters
from ..transformations.raw_converters_to_calibrated import transform_raw_converter


# TODO: Documentation
# noinspection PyUnresolvedReferences
def raw_converter_to_calibrated_hdulist(converter):
    # type: (SingleCCDRawConverter) -> HDUList
    """
    TODO: Document me

    :param converter:
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

    header_with_parameters = set_header_settings(
        converter.parameters,
        raw_converter_parameters,
        converter.conversion_metadata.header)
    header_with_transformation_flags = set_header_settings(
        converter.flags,
        raw_transformation_flags,
        header_with_parameters)
    header_with_added_history = add_command_to_header_history(
        converter.conversion_metadata.command,
        header_with_transformation_flags) \
        if isinstance(converter.conversion_metadata.command, str) else header_with_transformation_flags

    return HDUList(PrimaryHDU(
        header=header_with_added_history,
        # `+` concatenates python lists
        data=numpy.hstack(left_dark_parts + image_parts + right_dark_parts),
    ))


# TODO: Documentation
def write_raw_converter_to_calibrated_fits(converter, output_file, checksum=True):
    # type: (SingleCCDRawConverter, str, bool) -> None
    """
    Write a completed :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter`
    to a calibrated FITS file.

    :param converter:
    :type converter: :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter`
    :param output_file:
    :type output_file: :py:class:`file` or :py:class:`str`
    :param checksum:
    :type checksum: bool
    :rtype: NoneType
    """
    hdulist = raw_converter_to_calibrated_hdulist(converter)

    try:
        os.remove(output_file)
    except OSError:
        pass

    hdulist.writeto(output_file, checksum=checksum)


# TODO: Documentation
def raw_converter_flags_from_fits_header(fits_header, flag_overrides=None):
    """
    Construct a :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverterFlags`
    from a FITS header.

    TODO: Document me

    :param fits_header: FITS header to use for parsing parameters
    :type fits_header: :py:class:`astropy.io.fits.Header`
    :param flag_overrides:
    :type flag_overrides: :py:class:`object` or :py:class:`dict`
    :rtype: :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverterFlags`
    """

    flag_override_object = namedtuple('FlagOverrides', flag_overrides.keys())(**flag_overrides) \
        if isinstance(flag_overrides, dict) else flag_overrides

    def get_flag(flag_name):
        return get_header_setting(
            flag_name,
            raw_transformation_flags,
            fits_header,
            getattr(flag_override_object, flag_name) if hasattr(flag_override_object, flag_name) else None)

    return SingleCCDRawConverterFlags(**{k: get_flag(k) for k in raw_transformation_flags})


# TODO: Documentation
def raw_converter_parameters_from_fits_header(fits_header, parameter_overrides=None):
    """
    TODO: Document this

    :param fits_header: FITS header to use for parsing parameters
    :type fits_header: :py:class:`astropy.io.fits.Header`
    :param parameter_overrides:
    :type parameter_overrides: :py:class:`object` or :py:class:`dict`
    :rtype: :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverterParameters`
    """

    parameter_overrides_object = namedtuple('ParameterOverrides', parameter_overrides.keys())(**parameter_overrides) \
        if isinstance(parameter_overrides, dict) else parameter_overrides

    def get_parameter(parameter_name):
        return get_header_setting(
            parameter_name,
            raw_converter_parameters,
            fits_header,
            getattr(parameter_overrides_object, parameter_name)
            if hasattr(parameter_overrides_object, parameter_name) else None)

    return SingleCCDRawConverterParameters(**{k: get_parameter(k) for k in raw_converter_parameters})


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
def raw_converter_from_hdulist(header_data_unit_list,
                               command=None,
                               origin_file_name=None,
                               flag_overrides=None,
                               parameter_overrides=None, ):
    """
    TODO: Document this

    :param header_data_unit_list:
    :param command:
    :param origin_file_name:
    :param flag_overrides:
    :type flag_overrides: :py:class:`object` or :py:class:`dict`
    :param parameter_overrides:
    :type parameter_overrides: :py:class:`object` or :py:class:`dict`
    :rtype: SingleCCDRawConverter
    """
    from numpy import hsplit, fliplr
    conversion_metadata = ConversionMetaData(
        origin_file_name=origin_file_name,
        command=command,
        header=header_data_unit_list[0].header)  # type: ConversionMetaData
    flag_overrides = raw_converter_flags_from_fits_header(
        conversion_metadata.header,
        flag_overrides=flag_overrides)
    parameters = raw_converter_parameters_from_fits_header(
        conversion_metadata.header,
        parameter_overrides=parameter_overrides)
    assert len(header_data_unit_list) == 1, "Only a single image per FITS file is supported"
    assert header_data_unit_list[0].data.shape[1] % parameters.number_of_slices == 0, \
        "Image did not have the specified number of slices"

    early_dark_pixel_count = parameters.number_of_slices * parameters.early_dark_pixel_columns
    late_dark_pixel_count = parameters.number_of_slices * parameters.late_dark_pixel_columns
    sliced_image_smear_and_dark_pixels = hsplit(
        header_data_unit_list[0].data[:, early_dark_pixel_count:-late_dark_pixel_count],
        parameters.number_of_slices)
    sliced_early_dark_pixels = hsplit(header_data_unit_list[0].data[:, :early_dark_pixel_count],
                                      parameters.number_of_slices)
    sliced_late_dark_pixels = hsplit(header_data_unit_list[0].data[:, -late_dark_pixel_count:],
                                     parameters.number_of_slices)

    # TODO: Document this in layout.rst
    # Rows in odd numbered slices have to be reversed
    for i in range(1, parameters.number_of_slices, 2):
        sliced_image_smear_and_dark_pixels[i] = fliplr(sliced_image_smear_and_dark_pixels[i])
        sliced_early_dark_pixels[i] = fliplr(sliced_early_dark_pixels[i])
        sliced_late_dark_pixels[i] = fliplr(sliced_late_dark_pixels[i])

    return SingleCCDRawConverter(
        slices=tuple(map(make_slice_from_raw_data,
                         sliced_image_smear_and_dark_pixels,
                         range(parameters.number_of_slices),
                         sliced_early_dark_pixels,
                         sliced_late_dark_pixels)),
        conversion_metadata=conversion_metadata,
        parameters=parameters,
        flags=flag_overrides,
    )


# TODO: Documentation
def raw_converter_from_fits(
        input_file,
        command=None,
        checksum=True,
        flag_overrides=None,
        parameter_overrides=None):
    """
    TODO: Document this


    :param input_file:
    :param command:
    :param checksum:
    :param flag_overrides:
    :type flag_overrides: :py:class:`object` or :py:class:`dict`
    :param parameter_overrides:
    :type parameter_overrides: :py:class:`object` or :py:class:`dict`
    :rtype:
    """
    return raw_converter_from_hdulist(
        astropy.io.fits.open(input_file, checksum=checksum),
        command=command,
        origin_file_name=input_file,
        flag_overrides=flag_overrides,
        parameter_overrides=parameter_overrides,
    )


def raw_fits_to_calibrated(
        fits_input_file,
        fits_output_file,
        command=None,
        checksum=True,
        flag_overrides=None,
        parameter_overrides=None,
        transformation_settings=None):
    """
    Read a raw FITS file in as input, with units specified in *Analogue to Digital Converter Units* (ADU),
    run a series of transformations over it, and output the results to a specified file.

    :param fits_input_file: A raw FITS file to use as input
    :type fits_input_file: str
    :param fits_output_file: A FITS file to use as output; will be clobbered if it exists
    :type fits_output_file: str
    :param command: The command issued to be recorded in the ``HISTORY`` header keyword in the output
    :type command: str
    :param checksum: Whether to use checksums for data validation in reading and writing
    :type checksum: bool
    :param flag_overrides: An object or dictionary specifying values transformation flags should take \
    rather than their defaults
    :type flag_overrides: :py:class:`object` or :py:class:`dict`
    :param parameter_overrides: An object or dictionary specifying values parameters should take \
    rather than their defaults
    :type parameter_overrides: :py:class:`object` or :py:class:`dict`
    :param transformation_settings: An object which specifies which transformations should run, rather than the defaults
    :type transformation_settings: object
    """
    single_ccd_raw_converter = raw_converter_from_fits(
        fits_input_file,
        command=command,
        checksum=checksum,
        flag_overrides=flag_overrides,
        parameter_overrides=parameter_overrides)
    write_raw_converter_to_calibrated_fits(
        transform_raw_converter(
            single_ccd_raw_converter,
            transformation_settings=transformation_settings),
        fits_output_file,
        checksum=checksum)
