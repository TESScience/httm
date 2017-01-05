"""
``httm.data_structures.electron_flux_converter``
================================================

This module contains data structures for dealing with converting electron flux images to raw images.
"""

from collections import namedtuple, OrderedDict

from .documentation import document_parameters
from .metadata import parameters, transformation_flags

electron_flux_converter_parameters = parameters

electron_flux_transformation_flags = OrderedDict((k, dict(default=False, **transformation_flags[k]))
                                                 for k in transformation_flags.keys())


# noinspection PyClassHasNoInit
class SingleCCDElectronFluxConverterParameters(namedtuple('SingleCCDElectronFluxConverterParameters',
                                                          electron_flux_converter_parameters.keys())):
    __doc__ = """
Converter parameters for converting a electron flux FITS image into a simulated raw FITS image.

Constructed using :py:func:`~httm.fits_utilities.electron_flux_fits.electron_flux_converter_from_fits` or
:py:func:`~httm.fits_utilities.electron_flux_fits.electron_flux_converter_from_hdulist`.

{parameter_documentation}
""".format(parameter_documentation=document_parameters(electron_flux_converter_parameters))
    __slots__ = ()


# noinspection PyClassHasNoInit
class SingleCCDElectronFluxConverterFlags(
    namedtuple('SingleCCDElectronFluxConverterFlags',
               electron_flux_transformation_flags.keys())):
    __doc__ = """
Flags indicating which raw transformations have been performed.

{flags_documentation}
""".format(flags_documentation=document_parameters(electron_flux_transformation_flags))
    __slots__ = ()


# noinspection PyUnresolvedReferences,PyClassHasNoInit
class SingleCCDElectronFluxConverter(
    namedtuple('SingleCCDElectronFluxConverter',
               ['slices', 'conversion_metadata', 'parameters', 'flags'])):
    """
    An immutable object for managing a transformation from a electron flux FITS image into a simulated raw image.

    :param slices: The slices of the image
    :type slices: tuple of :py:class:`~httm.data_structures.common.Slice` objects
    :param conversion_metadata: Meta data associated with the image conversion
    :type conversion_metadata: :py:class:`~httm.data_structures.common.ConversionMetaData`
    :param parameters: The parameters of the transformation
    :type parameters: :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverterParameters`
    :param flags: Flags indicating the state of the transformation
    :type flags: :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverterFlags`
    """
    __slots__ = ()
