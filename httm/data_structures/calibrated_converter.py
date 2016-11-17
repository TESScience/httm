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

calibrated_transformations = OrderedDict([
    ('introduce_smear_rows', {
        'type': 'bool',
        'default': True,
        'documentation': 'Introduce *smear rows* to each slice of the image.',
    }),
    ('add_shot_noise', {
        'type': 'bool',
        'default': True,
        'documentation': 'Add *shot noise* to each pixel in each slice of the image.',
    }),
    ('simulate_blooming', {
        'type': 'bool',
        'default': True,
        'documentation': 'Simulate *blooming* on for each column for each slice of the image.',
    }),
    ('add_readout_noise', {
        'type': 'bool',
        'default': True,
        'documentation': 'Add *readout noise* to each pixel in each slice of the image.',
    }),
    ('simulate_undershoot', {
        'type': 'bool',
        'default': True,
        'documentation': 'Simulate *undershoot* on each row of each slice in the image.',
    }),
    ('simulate_start_of_line_ringing', {
        'type': 'bool',
        'default': True,
        'documentation': 'Simulate *start of line ringing* on each row of each slice in the image.',
    }),
    ('add_pattern_noise', {
        'type': 'bool',
        'default': True,
        'documentation': 'Add a fixed *pattern noise* to each slice in the image.',
    }),
    ('add_baseline', {
        'type': 'bool',
        'default': True,
        'documentation': 'Add a *baseline electron count* to each slice in the image.',
    }),
    ('convert_electrons_to_adu', {
        'type': 'bool',
        'default': True,
        'documentation': 'Convert the image from having pixel units in electron counts to '
                         '*Analogue to Digital Converter Units* (ADU).',
    }),
])


# noinspection PyClassHasNoInit
class SingleCCDCalibratedTransformations(namedtuple('SingleCCDCalibratedConverterParameters',
                                                    calibrated_transformations.keys())):
    __doc__ = """
Designate which transformations to run when processing a
:py:class:`~httm.data_structures.calibrated_converter.SingleCCDCalibratedConverter`.

See the :mod:`httm.transformations.calibrated_converters_to_raw` documentation for details.

{parameter_documentation}
""".format(parameter_documentation=document_parameters(calibrated_transformations))
    __slots__ = ()


SingleCCDCalibratedTransformations.__new__.__defaults__ = \
    tuple(transformation["default"] for transformation in calibrated_transformations.values())


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
