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
``httm.data_structures.raw_converter``
=============================================

This module contains data structures for dealing with converting raw images to calibrated images.
"""

from collections import namedtuple, OrderedDict

from .documentation import document_parameters
from .metadata import transformation_flags, parameters

raw_converter_parameters = OrderedDict((k, parameters[k])
                                       for k in ['number_of_slices',
                                                 'camera_number',
                                                 'ccd_number',
                                                 'number_of_exposures',
                                                 'video_scales',
                                                 'early_dark_pixel_columns',
                                                 'late_dark_pixel_columns',
                                                 'final_dark_pixel_rows',
                                                 'smear_rows',
                                                 'gain_loss',
                                                 'undershoot_parameter',
                                                 'pattern_noise'
                                                 ])

raw_transformation_flags = OrderedDict((k, dict(default=True, **transformation_flags[k]))
                                       for k in ['smear_rows_present',
                                                 'undershoot_present',
                                                 'pattern_noise_present',
                                                 'start_of_line_ringing_present',
                                                 'baseline_present',
                                                 'in_adu'])


# noinspection PyUnresolvedReferences
class SingleCCDRawConverterParameters(
    namedtuple('SingleCCDRawConverterParameters',
               raw_converter_parameters.keys())):
    __doc__ = """
Converter parameters for converting a raw FITS image into a calibrated FITS image.

Constructed using :py:func:`~httm.fits_utilities.raw_fits.raw_converter_parameters_from_fits_header`.

{parameter_documentation}
""".format(parameter_documentation=document_parameters(raw_converter_parameters))
    __slots__ = ()


# noinspection PyClassHasNoInit
class SingleCCDRawConverterFlags(
    namedtuple('SingleCCDRawConverterFlags',
               raw_transformation_flags.keys())):
    __doc__ = """
Flags indicating which raw transformations have been performed.

{parameter_documentation}
""".format(parameter_documentation=document_parameters(raw_transformation_flags))
    __slots__ = ()


# noinspection PyUnresolvedReferences,PyClassHasNoInit
class SingleCCDRawConverter(
    namedtuple('SingleCCDRawConverter',
               ['slices',
                'conversion_metadata',
                'parameters',
                'flags'])):
    """
    An immutable object for managing a transformation from a raw FITS image into a calibrated image.

    :param slices: The slices of the image
    :type slices: list of :py:class:`~httm.data_structures.common.Slice` objects
    :param conversion_metadata: Meta data associated with the image transformation
    :type conversion_metadata: :py:class:`~httm.data_structures.common.ConversionMetaData`
    :param parameters: The parameters of the transformation
    :type parameters: :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverterParameters`
    :param flags: Flags indicating the state of the transformation
    :type flags: :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverterFlags`
    """
    __slots__ = ()
