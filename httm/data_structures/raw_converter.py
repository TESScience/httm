"""
``httm.data_structures.raw_converter``
=============================================

This module contains data structures for dealing with converting raw images to calibrated images.
"""

from collections import namedtuple, OrderedDict

from documentation import document_parameters
from metadata import transformation_flags, parameters

raw_converter_parameters = OrderedDict((k, parameters[k])
                                       for k in ['number_of_slices',
                                                 'camera_number',
                                                 'ccd_number',
                                                 'number_of_exposures',
                                                 'video_scales',
                                                 'left_dark_pixel_columns',
                                                 'right_dark_pixel_columns',
                                                 'top_dark_pixel_rows',
                                                 'smear_rows',
                                                 'gain_loss',
                                                 'undershoot_parameter',
                                                 'pattern_noise'])

raw_transformation_flags = OrderedDict((k, dict(default=True, **transformation_flags[k]))
                                       for k in ['smear_rows_present',
                                                 'undershoot_present',
                                                 'pattern_noise_present',
                                                 'start_of_line_ringing_present'])


# noinspection PyUnresolvedReferences
class SingleCCDRawConverterParameters(
    namedtuple('SingleCCDRawConverterParameters',
               raw_converter_parameters.keys())):
    __doc__ = """
Converter parameters for converting a raw FITS image into a calibrated FITS image.

Constructed using :py:func:`~httm.fits_utilities.raw_fits.raw_converter_parameters_from_fits`.

{parameter_documentation}
""".format(parameter_documentation=document_parameters(raw_converter_parameters))
    __slots__ = ()


# TODO derive SingleCCDRawConverterFlags from FITS header
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
                'fits_metadata',
                'parameters',
                'flags'])):
    """
    An immutable object for managing a transformation from a raw FITS image into a calibrated image.

    :param slices: The slices of the image
    :type slices: list of :py:class:`~httm.data_structures.common.Slice` objects
    :param fits_metadata: Meta data associated with the image
    :type fits_metadata: :py:class:`~httm.data_structures.common.FITSMetaData`
    :param parameters: The parameters of the transformation
    :type parameters: :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverterParameters`
    :param flags: Flags indicating the state of the transformation
    :type flags: :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverterFlags`
    """
    __slots__ = ()
