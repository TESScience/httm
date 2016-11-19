"""
``httm.transformations.raw_converters_to_calibrated``
=====================================================

Transformation functions for processing
:py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter` objects so that
they are suitable for writing to a calibrated FITS file.

"""
from collections import OrderedDict

from .raw_slices_to_calibrated import convert_slice_adu_to_electrons, remove_pattern_noise_from_slice, \
    remove_undershoot_from_slice, remove_smear_from_slice
from ..resource_utilities import load_npz_resource


# TODO: Add flags, specify which remove baseline electron count


def convert_adu_to_electrons(raw_converter):
    # type: (SingleCCDRawConverter) -> SingleCCDRawConverter
    """
    Converts a :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter` from
    having *Analogue to Digital Converter Units* (ADU) to estimated electron counts by calling
    :py:func:`~httm.transformations.raw_slices_to_calibrated.convert_slice_adu_to_electrons` over each slice.

    :param raw_converter: Should have *Analogue to Digital Converter Units* (ADU) \
    for units for each of its slices
    :type raw_converter: :py:class:`~httm.data_structures.calibrated_converter.SingleCCDCalibratedConverter`
    :rtype: :py:class:`~httm.data_structures.calibrated_converter.SingleCCDCalibratedConverter`
    """
    image_slices = raw_converter.slices
    video_scales = raw_converter.parameters.video_scales
    assert len(video_scales) >= len(image_slices), "There should be at least as many video scales as slices"
    number_of_exposures = raw_converter.parameters.number_of_exposures
    gain_loss = raw_converter.parameters.gain_loss
    # noinspection PyProtectedMember
    return raw_converter._replace(
        slices=tuple(convert_slice_adu_to_electrons(gain_loss, number_of_exposures, video_scale, image_slice)
                     for (video_scale, image_slice) in zip(video_scales, image_slices)))


def remove_pattern_noise(raw_converter):
    # type: (SingleCCDRawConverter) -> SingleCCDRawConverter
    """
    Compensates for a fixed pattern noise, that varies from slice to slice, on a
    :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter`
    by calling :py:func:`~httm.transformations.raw_slices_to_calibrated.remove_pattern_noise_from_slice`
    over each slice.

    :param raw_converter: Should have electrons for units for each of its slices
    :type raw_converter: :py:class:`~httm.data_structures.calibrated_converter.SingleCCDCalibratedConverter`
    :rtype: :py:class:`~httm.data_structures.calibrated_converter.SingleCCDCalibratedConverter`
    """
    pattern_noises = load_npz_resource(raw_converter.parameters.pattern_noise, 'pattern_noise')
    image_slices = raw_converter.slices
    assert len(pattern_noises) >= len(image_slices), "There should be at least as many noise patterns as slices"
    # noinspection PyProtectedMember
    return raw_converter._replace(
        slices=tuple(remove_pattern_noise_from_slice(pattern_noise, image_slice)
                     for (pattern_noise, image_slice) in zip(pattern_noises, image_slices)))


def remove_start_of_line_ringing(raw_converter):
    # type: (SingleCCDRawConverter) -> SingleCCDRawConverter
    """
    Compensates for *start of line ringing* on each row in a
    :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter`
    by calling :py:func:`~httm.transformations.raw_slices_to_calibrated.remove_start_of_line_ringing_from_slice`
    over each slice.

    :param raw_converter: Should have electrons for units for each of its slices
    :type raw_converter: :py:class:`~httm.data_structures.calibrated_converter.SingleCCDCalibratedConverter`
    :rtype: :py:class:`~httm.data_structures.calibrated_converter.SingleCCDCalibratedConverter`
    """
    top_dark_pixel_rows = raw_converter.parameters.top_dark_pixel_rows
    image_slices = raw_converter.slices
    # noinspection PyProtectedMember
    return raw_converter._replace(
        slices=tuple(remove_pattern_noise_from_slice(top_dark_pixel_rows, image_slice)
                     for image_slice in image_slices))


def remove_undershoot(raw_converter):
    # type: (SingleCCDRawConverter) -> SingleCCDRawConverter
    """
    Removes *undershoot* from each row in a
    :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter`
    by calling :py:func:`~httm.transformations.raw_slices_to_calibrated.remove_undershoot_from_slice`
    over each slice.

    :param raw_converter: Should have electrons for units for each of its slices
    :type raw_converter: :py:class:`~httm.data_structures.calibrated_converter.SingleCCDCalibratedConverter`
    :rtype: :py:class:`~httm.data_structures.calibrated_converter.SingleCCDCalibratedConverter`
    """
    undershoot_parameter = raw_converter.parameters.undershoot_parameter
    image_slices = raw_converter.slices
    # noinspection PyProtectedMember
    return raw_converter._replace(
        slices=tuple(remove_undershoot_from_slice(undershoot_parameter, image_slice)
                     for image_slice in image_slices))


def remove_smear(raw_converter):
    # type: (SingleCCDRawConverter) -> SingleCCDRawConverter
    """
    Removes *smear* and zeroes the *smear rows* in a
    :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter`
    by calling :py:func:`~httm.transformations.raw_slices_to_calibrated.remove_smear_from_slice`
    over each slice.

    :param raw_converter: Should have electrons for units for each of its slices
    :type raw_converter: :py:class:`~httm.data_structures.calibrated_converter.SingleCCDCalibratedConverter`
    :rtype: :py:class:`~httm.data_structures.calibrated_converter.SingleCCDCalibratedConverter`
    """
    top_dark_pixel_rows = raw_converter.parameters.top_dark_pixel_rows
    smear_rows = raw_converter.parameters.smear_rows
    right_dark_pixel_columns = raw_converter.parameters.right_dark_pixel_columns
    left_dark_pixel_columns = raw_converter.parameters.left_dark_pixel_columns
    image_slices = raw_converter.slices
    # noinspection PyProtectedMember
    return raw_converter._replace(
        slices=tuple(remove_smear_from_slice(left_dark_pixel_columns, right_dark_pixel_columns,
                                             top_dark_pixel_rows, smear_rows, image_slice)
                     for image_slice in image_slices))


raw_transformations = OrderedDict([
    ('convert_adu_to_electrons', {
        'default': True,
        'documentation': 'Convert the image from having units in '
                         '*Analogue to Digital Converter Units* (ADU) '
                         'to electron counts.',
        'function': convert_adu_to_electrons,
    }),
    ('remove_pattern_noise', {
        'default': True,
        'documentation': 'Compensate for a fixed *pattern noise* on each slice of the image.',
        'function': remove_pattern_noise,
    }),
    ('remove_start_of_line_ringing', {
        'default': True,
        'documentation': 'Compensate for *start of line ringing* on each row of each slice of the image.',
        'function': remove_start_of_line_ringing,
    }),
    ('remove_undershoot', {
        'default': True,
        'documentation': 'Compensate for *undershoot* for each row of each slice of the image.',
        'function': remove_undershoot,
    }),
    ('remove_smear', {
        'default': True,
        'documentation': 'Compensate for *smear* in the image by reading it from the '
                         '*smear rows* each slice and removing it from the rest of the slice.',
        'function': remove_smear,
    }),
])

raw_transformation_defaults = OrderedDict(
    (key, raw_transformations[key]['default'])
    for key in raw_transformations.keys()
)

raw_transformation_functions = OrderedDict(
    (key, raw_transformations[key]['function'])
    for key in raw_transformations.keys()
)

