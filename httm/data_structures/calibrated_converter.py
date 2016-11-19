"""
``httm.data_structures.calibrated_converter``
=============================================

This module contains data structures for dealing with converting calibrated images to raw images.
"""

from collections import namedtuple, OrderedDict

from .documentation import document_parameters
from .metadata import parameters, transformation_flags

calibrated_converter_parameters = parameters

calibrated_transformation_flags = OrderedDict((k, dict(default=False, **transformation_flags[k]))
                                              for k in transformation_flags.keys())


# noinspection PyClassHasNoInit
class SingleCCDCalibratedConverterParameters(namedtuple('SingleCCDCalibratedConverterParameters',
                                                        calibrated_converter_parameters.keys())):
    __doc__ = """
Converter parameters for converting a calibrated FITS image into an uncalibrated FITS image.

Constructed using :py:func:`~httm.fits_utilities.calibrated_fits.calibrated_converter_from_fits` or
:py:func:`~httm.fits_utilities.calibrated_fits.calibrated_converter_from_HDUList`.

{parameter_documentation}
""".format(parameter_documentation=document_parameters(calibrated_converter_parameters))
    __slots__ = ()


# TODO derive SingleCCDCalibratedConverterFlags from FITS header
# noinspection PyClassHasNoInit
class SingleCCDCalibratedConverterFlags(
    namedtuple('SingleCCDCalibratedConverterFlags',
               calibrated_transformation_flags.keys())):
    __doc__ = """
Flags indicating which raw transformations have been performed.

{parameter_documentation}
""".format(parameter_documentation=document_parameters(calibrated_transformation_flags))
    __slots__ = ()


# noinspection PyUnresolvedReferences,PyClassHasNoInit
class SingleCCDCalibratedConverter(
    namedtuple('SingleCCDCalibratedConverter',
               ['slices',
                'fits_metadata',
                'parameters',
                'flags'])):
    """
    An immutable object for managing a transformation from a calibrated FITS image into a (simulated) raw image.

    :param slices: The slices of the image
    :type slices: tuple of :py:class:`~httm.data_structures.common.Slice` objects
    :param fits_metadata: Meta data associated with the image
    :type fits_metadata: :py:class:`~httm.data_structures.common.FITSMetaData`
    :param parameters: The parameters of the transformation
    :type parameters: :py:class:`~httm.data_structures.calibrated_converter.SingleCCDCalibratedConverterParameters`
    :param flags: Flags indicating the state of the transformation
    :type flags: :py:class:`~httm.data_structures.calibrated_converter.SingleCCDCalibratedConverterFlags`
    """
    __slots__ = ()
