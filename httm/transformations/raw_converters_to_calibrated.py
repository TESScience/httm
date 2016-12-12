"""
``httm.transformations.raw_converters_to_calibrated``
=====================================================

Transformation functions for processing
:py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter` objects so that
they are suitable for writing to a calibrated FITS file.

"""
from collections import OrderedDict

from .raw_slices_to_calibrated import convert_slice_adu_to_electrons, remove_pattern_noise_from_slice, \
    remove_undershoot_from_slice, remove_smear_from_slice, remove_baseline_from_slice
from ..resource_utilities import load_npz_resource
from ..data_structures.raw_converter import SingleCCDRawConverter

# TODO: Add flags, specify which remove baseline electron count


def convert_adu_to_electrons(raw_converter):
    # type: (SingleCCDRawConverter) -> SingleCCDRawConverter
    """
    Converts a :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter` from
    having *Analogue to Digital Converter Units* (ADU) to estimated electron counts by calling
    :py:func:`~httm.transformations.raw_slices_to_calibrated.convert_slice_adu_to_electrons` over each slice.

    :param raw_converter: Should have *Analogue to Digital Converter Units* (ADU) \
    for units for each of its slices
    :type raw_converter: :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`
    :rtype: :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`
    """
    assert raw_converter.flags.in_adu, "Input should be in *Analogue to Digital Converter Units* (ADU)"
    image_slices = raw_converter.slices
    video_scales = raw_converter.parameters.video_scales
    assert len(video_scales) >= len(image_slices), "There should be at least as many video scales as slices"
    number_of_exposures = raw_converter.parameters.number_of_exposures
    gain_loss = raw_converter.parameters.gain_loss
    # noinspection PyProtectedMember
    return raw_converter._replace(
        slices=tuple(convert_slice_adu_to_electrons(gain_loss, number_of_exposures, video_scale, image_slice)
                     for (video_scale, image_slice) in zip(video_scales, image_slices)),
        flags=raw_converter.flags._replace(in_adu=True)
    )


def remove_baseline(raw_converter):
    # type: (SingleCCDRawConverter) -> SingleCCDRawConverter
    """
    This function estimates *baseline* from the *dark pixels* for each slice in a
    :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`
    and compensates for this effect. Calls
    :py:func:`~httm.transformations.raw_slices_to_calibrated.remove_baseline_from_slice` over each slice.

    :param raw_converter: Should have *Analogue to Digital Converter Units* (ADU) \
    for units for each of its slices
    :type raw_converter: :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`
    :rtype: :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`
    """
    image_slices = raw_converter.slices
    early_dark_pixel_columns = raw_converter.parameters.early_dark_pixel_columns
    late_dark_pixel_columns = raw_converter.parameters.late_dark_pixel_columns
    # noinspection PyProtectedMember
    return raw_converter._replace(
        slices=tuple(remove_baseline_from_slice(early_dark_pixel_columns, late_dark_pixel_columns, image_slice)
                     for image_slice in image_slices), flags=raw_converter.flags._replace(baseline_present=False))


def remove_pattern_noise(raw_converter):
    # type: (SingleCCDRawConverter) -> SingleCCDRawConverter
    """
    Compensates for a fixed pattern noise, that varies from slice to slice, on a
    :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter`
    by calling :py:func:`~httm.transformations.raw_slices_to_calibrated.remove_pattern_noise_from_slice`
    over each slice.

    :param raw_converter: Should have electrons for units for each of its slices
    :type raw_converter: :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`
    :rtype: :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`
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
    :type raw_converter: :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`
    :rtype: :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`
    """
    final_dark_pixel_rows = raw_converter.parameters.final_dark_pixel_rows
    image_slices = raw_converter.slices
    # noinspection PyProtectedMember
    return raw_converter._replace(
        slices=tuple(remove_pattern_noise_from_slice(final_dark_pixel_rows, image_slice)
                     for image_slice in image_slices))


def remove_undershoot(raw_converter):
    # type: (SingleCCDRawConverter) -> SingleCCDRawConverter
    """
    Removes *undershoot* from each row in a
    :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter`
    by calling :py:func:`~httm.transformations.raw_slices_to_calibrated.remove_undershoot_from_slice`
    over each slice.

    :param raw_converter: Should have electrons for units for each of its slices
    :type raw_converter: :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`
    :rtype: :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`
    """
    assert raw_converter.flags.baseline_present == False, "Baseline should be removed before removing undershoot"

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
    :type raw_converter: :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`
    :rtype: :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`
    """
    final_dark_pixel_rows = raw_converter.parameters.final_dark_pixel_rows
    smear_rows = raw_converter.parameters.smear_rows
    late_dark_pixel_columns = raw_converter.parameters.late_dark_pixel_columns
    early_dark_pixel_columns = raw_converter.parameters.early_dark_pixel_columns
    image_slices = raw_converter.slices
    # noinspection PyProtectedMember
    return raw_converter._replace(
        slices=tuple(remove_smear_from_slice(early_dark_pixel_columns, late_dark_pixel_columns,
                                             final_dark_pixel_rows, smear_rows, image_slice)
                     for image_slice in image_slices))


raw_transformations = OrderedDict([
    ('convert_adu_to_electrons', {
        'default': True,
        'documentation': 'Convert the image from having units in '
                         '*Analogue to Digital Converter Units* (ADU) '
                         'to electron counts.',
        'function': convert_adu_to_electrons,
    }),
    ('remove_baseline', {
        'default': True,
        'documentation': 'This averages the pixels in the dark columns and subtracts ' +
                         'the result from each pixel in the image.',
        'function': remove_baseline,
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

raw_transformation_default_settings = OrderedDict(
    (key, raw_transformations[key]['default'])
    for key in raw_transformations.keys()
)

raw_transformation_functions = OrderedDict(
    (key, raw_transformations[key]['function'])
    for key in raw_transformations.keys()
)
