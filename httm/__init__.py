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
``httm``
========

This module contains top level transformations for converting electron flux
to raw TESS full frame FITS images and raw to calibrated TESS full frame FITS
images.
"""

from .fits_utilities.electron_flux_fits import \
    electron_flux_converter_from_fits, \
    write_electron_flux_converter_to_simulated_raw_fits
from .fits_utilities.raw_fits import raw_converter_from_fits, write_raw_converter_to_calibrated_fits
from .transformations.electron_flux_converters_to_raw import transform_electron_flux_converter
from .transformations.raw_converters_to_calibrated import transform_raw_converter


def raw_fits_to_calibrated(
        fits_input_file,
        fits_output_file,
        command=None,
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
    :param flag_overrides: An object specifying values transformation flags should take rather than their defaults
    :type flag_overrides: object
    :param parameter_overrides: An object specifying values parameters should take rather than their defaults
    :type parameter_overrides: object
    :param transformation_settings: An object which transformations should run, rather than the defaults
    :type transformation_settings: object
    """
    single_ccd_raw_converter = raw_converter_from_fits(
        fits_input_file,
        command=command,
        flag_overrides=flag_overrides,
        parameter_overrides=parameter_overrides)
    write_raw_converter_to_calibrated_fits(
        transform_raw_converter(
            single_ccd_raw_converter,
            transformation_settings=transformation_settings),
        fits_output_file)


def electron_flux_fits_to_raw(
        fits_input_file,
        fits_output_file,
        command=None,
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
    :param flag_overrides: An object specifying values transformation flags should take rather than their defaults
    :type flag_overrides: object
    :param parameter_overrides: An object specifying values parameters should take rather than their defaults
    :type parameter_overrides: object
    :param transformation_settings: An object which transformations should run, rather than the defaults
    :type transformation_settings: object
    """
    single_ccd_electron_flux_converter = electron_flux_converter_from_fits(
        fits_input_file,
        command=command,
        flag_overrides=flag_overrides,
        parameter_overrides=parameter_overrides)
    write_electron_flux_converter_to_simulated_raw_fits(
        transform_electron_flux_converter(
            single_ccd_electron_flux_converter,
            transformation_settings=transformation_settings),
        fits_output_file)
