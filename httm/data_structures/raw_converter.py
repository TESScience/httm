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
                                                 'video_scales',
                                                 'compression',
                                                 'undershoot',
                                                 'pattern_noise'])

raw_transformation_flags = OrderedDict((k, dict(default=True, **transformation_flags[k]))
                                       for k in ['smear_rows_present',
                                                 'undershoot_uncompensated',
                                                 'pattern_noise_uncompensated',
                                                 'start_of_line_ringing_uncompensated'])


# noinspection PyUnresolvedReferences
class RAWConverterParameters(
    namedtuple('RAWConverterParameters',
               raw_converter_parameters.keys())):
    __doc__ = """
Converter parameters for converting a calibrated FITS image into an uncalibrated FITS image.

Constructed using the parameters handed to :py:func:`~httm.raw_transform_from_file`.

{parameter_documentation}
""".format(parameter_documentation=document_parameters(raw_converter_parameters))
    __slots__ = ()


# TODO derive RawConverterFlags from FITS header
# noinspection PyClassHasNoInit
class RawConverterFlags(
    namedtuple('RawConverterFlags',
               raw_transformation_flags.keys())):
    __doc__ = """
Flags indicating which raw transformations have been performed.

{parameter_documentation}
""".format(parameter_documentation=document_parameters(raw_transformation_flags))
    __slots__ = ()


# noinspection PyUnresolvedReferences,PyClassHasNoInit
class RAWConverter(
    namedtuple('RAWConverter',
               ['slices',
                'fits_metadata',
                'parameters',
                'flags'])):
    """
    An immutable object for managing a transformation from a raw FITS image into a calibrated image.

    :param slices: The slices of the image
    :type slices: list of :py:class:`~httm.data_structures.common.Slice` objects
    :param fits_metadata: Meta data associated with the image
    :type fits_metadata: :py:class:`~httm.data_structures.FITSMetaData`
    :param parameters: The parameters of the transformation
    :type parameters: :py:class:`~httm.data_structures.raw_converter.RAWConverterParameters`
    :param flags: Flags indicating the state of the transformation
    :type flags: :py:class:`~httm.data_structures.RawConverterFlags`
    """
    __slots__ = ()
