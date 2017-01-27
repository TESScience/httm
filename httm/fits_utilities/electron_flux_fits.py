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


# noinspection SpellCheckingInspection
"""
``httm.fits_utilities.electron_flux_fits``
==========================================

This module contains functions for marshalling and de-marshalling
:py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`
and the other book-keeping objects it contains to and from FITS files or :py:class:`astropy.io.fits.HDUList` objects.
"""

import os
from collections import namedtuple

import astropy
import numpy
from astropy.io.fits import HDUList, PrimaryHDU, Header

from .header_tools import get_header_setting, set_header_settings, add_command_to_header_history
from ..data_structures.common import Slice, ConversionMetaData
from ..data_structures.electron_flux_converter import \
    SingleCCDElectronFluxConverterFlags, SingleCCDElectronFluxConverterParameters, \
    SingleCCDElectronFluxConverter, electron_flux_transformation_flags, electron_flux_converter_parameters
from ..transformations.electron_flux_converters_to_raw import transform_electron_flux_converter


# TODO: Documentation
# noinspection SpellCheckingInspection
def make_slice_from_electron_flux_data(
        pixels,
        early_dark_pixel_columns,
        late_dark_pixel_columns,
        final_dark_pixel_rows,
        smear_rows,
        index):
    # type: (numpy.ndarray, int, int, int, int, int) -> Slice
    """
    Construct a slice from an array of electron flux pixel data given a specified index.

    Result is in *electron counts*.

    :param pixels: Image pixels from the electron flux data
    :type pixels: :py:class:`numpy.ndarray`
    :param early_dark_pixel_columns:
    :type early_dark_pixel_columns: int
    :param late_dark_pixel_columns:
    :type late_dark_pixel_columns: int
    :param final_dark_pixel_rows:
    :type final_dark_pixel_rows: int
    :param smear_rows:
    :type smear_rows: int
    :param index: The index of the slice to construct
    :type index: int
    :rtype: :py:class:`~httm.data_structures.common.Slice`
    """
    image_and_smear_and_final_dark_pixels = numpy.vstack(
        [pixels, numpy.zeros((final_dark_pixel_rows + smear_rows, pixels.shape[1]))])
    row_count = image_and_smear_and_final_dark_pixels.shape[0]
    early_dark_pixels = numpy.zeros((row_count, early_dark_pixel_columns))
    late_dark_pixels = numpy.zeros((row_count, late_dark_pixel_columns))
    return Slice(
        pixels=numpy.hstack([early_dark_pixels, image_and_smear_and_final_dark_pixels, late_dark_pixels]),
        index=index,
        units='electrons',
    )


# TODO: Documentation
# noinspection SpellCheckingInspection
def electron_flux_converter_flags_from_fits_header(fits_header, flag_overrides=None):
    # type: (Header, object) -> SingleCCDElectronFluxConverterFlags
    """
    Construct a :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverterFlags`
    from a file or file name.

    :param fits_header: The file or file name to input
    :type fits_header: :py:class:`astropy.io.fits.Header`
    :param flag_overrides:
    :type flag_overrides: :py:class:`object` or :py:class:`dict`
    :rtype: :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverterFlags`
    """

    flag_override_object = namedtuple('FlagOverrides', flag_overrides.keys())(**flag_overrides) \
        if isinstance(flag_overrides, dict) else flag_overrides

    def get_flag(flag_name):
        return get_header_setting(
            flag_name,
            electron_flux_transformation_flags,
            fits_header,
            getattr(flag_override_object, flag_name) if hasattr(flag_override_object, flag_name) else None)

    return SingleCCDElectronFluxConverterFlags(**{k: get_flag(k) for k in electron_flux_transformation_flags})


# TODO: Documentation
# noinspection SpellCheckingInspection
def electron_flux_converter_parameters_from_fits_header(fits_header, parameter_overrides=None):
    # type: (Header, object) -> SingleCCDElectronFluxConverterParameters
    """
    TODO: Document me

    :param fits_header: FITS header to use for parsing parameters
    :type fits_header: :py:class:`astropy.io.fits.Header`
    :param parameter_overrides:
    :type parameter_overrides: :py:class:`object` or :py:class:`dict`
    :rtype: :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverterParameters`
    """

    parameter_overrides_object = namedtuple('ParameterOverrides', parameter_overrides.keys())(**parameter_overrides) \
        if isinstance(parameter_overrides, dict) else parameter_overrides

    def get_parameter(parameter_name):
        return get_header_setting(
            parameter_name,
            electron_flux_converter_parameters,
            fits_header,
            getattr(parameter_overrides_object, parameter_name)
            if hasattr(parameter_overrides_object, parameter_name) else None)

    return SingleCCDElectronFluxConverterParameters(
        **{k: get_parameter(k) for k in electron_flux_converter_parameters}
    )


# noinspection SpellCheckingInspection
def electron_flux_converter_to_simulated_raw_hdulist(converter):
    # type: (SingleCCDElectronFluxConverter) -> HDUList
    """
    This function converts a :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`
    into an :py:class:`astropy.io.fits.HDUList` object, suitable for writing out to a simulated raw FITS file.

    :param converter: An electron flux converter object
    :type converter: :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`
    :rtype: :py:class:`astropy.io.fits.HDUList`
    """
    early_dark_pixel_columns = converter.parameters.early_dark_pixel_columns
    late_dark_pixel_columns = converter.parameters.late_dark_pixel_columns
    final_dark_pixel_rows = converter.parameters.final_dark_pixel_rows
    smear_rows = converter.parameters.smear_rows
    slices = [
        raw_slice.pixels[:-(final_dark_pixel_rows + smear_rows), early_dark_pixel_columns:-late_dark_pixel_columns]
        for raw_slice in converter.slices]
    for i in range(1, len(slices), 2):
        slices[i] = numpy.fliplr(slices[i])
    header_with_parameters = set_header_settings(
        converter.parameters,
        electron_flux_converter_parameters,
        converter.conversion_metadata.header)
    header_with_transformation_flags = set_header_settings(
        converter.flags,
        electron_flux_transformation_flags,
        header_with_parameters)
    header_with_added_history = add_command_to_header_history(
        converter.conversion_metadata.command,
        header_with_transformation_flags) \
        if isinstance(converter.conversion_metadata.command, str) else header_with_transformation_flags
    return HDUList(PrimaryHDU(header=header_with_added_history,
                              data=numpy.hstack(slices)))


# TODO: Documentation
# noinspection SpellCheckingInspection
def write_electron_flux_converter_to_simulated_raw_fits(converter, output_file, checksum=True):
    # type: (SingleCCDElectronFluxConverter, str) -> None
    """
    Write a :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`
    to a simulated raw FITS file.

    Called for effect.

    :param converter: An electron flux converter object
    :type converter: :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`
    :param output_file:
    :type output_file: str
    :param checksum:
    :type checksum: bool
    :rtype: NoneType
    """
    hdulist = electron_flux_converter_to_simulated_raw_hdulist(converter)

    try:
        os.remove(output_file)
    except OSError:
        pass

    hdulist.writeto(output_file, checksum=checksum)


# TODO: Documentation
# noinspection PyUnresolvedReferences,SpellCheckingInspection
def electron_flux_converter_from_hdulist(
        header_data_unit_list,
        command=None,
        origin_file_name=None,
        flag_overrides=None,
        parameter_overrides=None):
    """
    TODO: Document me

    :param header_data_unit_list:
    :param command:
    :param origin_file_name:
    :param flag_overrides:
    :type flag_overrides: :py:class:`object` or :py:class:`dict`
    :param parameter_overrides:
    :type parameter_overrides: :py:class:`object` or :py:class:`dict`
    :rtype: :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`
    """
    conversion_metadata = ConversionMetaData(command=command,
                                             origin_file_name=origin_file_name,
                                             header=header_data_unit_list[0].header)  # type: ConversionMetaData
    flag_overrides = electron_flux_converter_flags_from_fits_header(conversion_metadata.header,
                                                                    flag_overrides=flag_overrides)
    parameters = electron_flux_converter_parameters_from_fits_header(conversion_metadata.header,
                                                                     parameter_overrides=parameter_overrides)
    assert len(header_data_unit_list) == 1, "Only a single image per FITS file is supported"
    assert header_data_unit_list[0].data.shape[1] % parameters.number_of_slices == 0, \
        "Image did not have the specified number of slices"
    return SingleCCDElectronFluxConverter(
        slices=tuple(
            map(lambda pixel_data, index:
                make_slice_from_electron_flux_data(pixel_data,
                                                   parameters.early_dark_pixel_columns,
                                                   parameters.late_dark_pixel_columns,
                                                   parameters.final_dark_pixel_rows,
                                                   parameters.smear_rows,
                                                   index),
                numpy.hsplit(header_data_unit_list[0].data, parameters.number_of_slices),
                range(parameters.number_of_slices))),
        conversion_metadata=conversion_metadata,
        parameters=parameters,
        flags=flag_overrides,
    )


# TODO: Documentation
def electron_flux_converter_from_fits(
        input_file,
        command=None,
        checksum=True,
        flag_overrides=None,
        parameter_overrides=None):
    """
    TODO: Document me

    :param input_file:
    :type input_file: str
    :param command:
    :type command: str
    :param checksum:
    :type checksum: bool
    :param flag_overrides:
    :type flag_overrides: :py:class:`object` or :py:class:`dict`
    :param parameter_overrides:
    :type parameter_overrides: :py:class:`object` or :py:class:`dict`
    :rtype:
    """
    return electron_flux_converter_from_hdulist(
        astropy.io.fits.open(input_file, checksum=checksum),
        command=command,
        origin_file_name=input_file,
        flag_overrides=flag_overrides,
        parameter_overrides=parameter_overrides,
    )


def electron_flux_fits_to_raw(
        fits_input_file,
        fits_output_file,
        command=None,
        checksum=True,
        flag_overrides=None,
        parameter_overrides=None,
        transformation_settings=None):
    """
    Read an electron flux FITS file in as input, with units specified in electron counts,
    run a series of transformations over it, and output the results to a specified file.

    :param fits_input_file: A FITS file with electron counts
    :type fits_input_file: str
    :param fits_output_file: A FITS file to use as output; will be clobbered if it exists
    :type fits_output_file: str
    :param command: The command issued to be recorded in the ``HISTORY`` header keyword in the output
    :type command: str
    :param checksum: Whether to use check-sums for data validation in reading and writing
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
    single_ccd_electron_flux_converter = electron_flux_converter_from_fits(
        fits_input_file,
        command=command,
        checksum=checksum,
        flag_overrides=flag_overrides,
        parameter_overrides=parameter_overrides)
    write_electron_flux_converter_to_simulated_raw_fits(
        transform_electron_flux_converter(
            single_ccd_electron_flux_converter,
            transformation_settings=transformation_settings),
        fits_output_file,
        checksum=checksum)
