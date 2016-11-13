"""
``httm.transformations.calibrated_converters_to_raw``
=====================================================

Transformation functions for processing
:py:class:`~httm.data_structures.calibrated_converter.CalibratedConverter` objects so that
they are suitable  for writing to a simulated raw FITS file.

"""
import calibrated_slices_to_raw
from ..resources import load_npz_resource


def introduce_smear_rows(calibrated_converter):
    # type: (CalibratedConverter) -> CalibratedConverter
    pass


def add_shot_noise(calibrated_converter):
    # type: (CalibratedConverter) -> CalibratedConverter
    pass


def simulate_blooming(calibrated_converter):
    # type: (CalibratedConverter) -> CalibratedConverter
    """
    Simulate *blooming* on a
    :py:class:`~httm.data_structures.calibrated_converter.CalibratedConverter` by calling
    :py:func:`~httm.transformations.calibrated_slices_to_raw.simulate_blooming_on_slice`
    over each slice.

    :param calibrated_converter: Should have electrons for units for each of its slices
    :type calibrated_converter: :py:class:`~httm.data_structures.calibrated_converter.CalibratedConverter`
    :rtype: :py:class:`~httm.data_structures.calibrated_converter.CalibratedConverter`
    """
    full_well = calibrated_converter.parameters.full_well
    blooming_threshold = calibrated_converter.parameters.blooming_threshold
    number_of_exposures = calibrated_converter.parameters.number_of_exposures
    image_slices = calibrated_converter.slices
    return calibrated_converter._replace(
        slices=tuple(map(lambda s: calibrated_slices_to_raw.simulate_blooming_on_slice(full_well, blooming_threshold,
                                                                                       number_of_exposures, s),
                         image_slices)))


def add_readout_noise(calibrated_converter):
    # type: (CalibratedConverter) -> CalibratedConverter
    """
    Add *readout noise* to a
    :py:class:`~httm.data_structures.calibrated_converter.CalibratedConverter` by calling
    :py:func:`~httm.transformations.calibrated_slices_to_raw.add_readout_noise_to_slice`
    over each slice.

    :param calibrated_converter: Should have electrons for units for each of its slices
    :type calibrated_converter: :py:class:`~httm.data_structures.calibrated_converter.CalibratedConverter`
    :rtype: :py:class:`~httm.data_structures.calibrated_converter.CalibratedConverter`
    """
    readout_noise_parameters = calibrated_converter.parameters.readout_noise_parameters
    image_slices = calibrated_converter.slices
    number_of_exposures = calibrated_converter.parameters.number_of_exposures
    return calibrated_converter._replace(
        slices=tuple(
            calibrated_slices_to_raw.add_readout_noise_to_slice(readout_noise_parameter, number_of_exposures,
                                                                image_slice)
            for (readout_noise_parameter, image_slice) in zip(readout_noise_parameters, image_slices)))


# noinspection PyProtectedMember
def simulate_undershoot(calibrated_converter):
    # type: (CalibratedConverter) -> CalibratedConverter
    """
    Add *undershoot* to a
    :py:class:`~httm.data_structures.calibrated_converter.CalibratedConverter` by calling
    :py:func:`~httm.transformations.calibrated_slices_to_raw.simulate_undershoot_on_slice`
    over each slice.

    :param calibrated_converter: Should have electrons for units for each of its slices
    :type calibrated_converter: :py:class:`~httm.data_structures.calibrated_converter.CalibratedConverter`
    :rtype: :py:class:`~httm.data_structures.calibrated_converter.CalibratedConverter`
    """
    undershoot_parameter = calibrated_converter.parameters.undershoot_parameter
    image_slices = calibrated_converter.slices
    return calibrated_converter._replace(
        slices=tuple(map(lambda s: calibrated_slices_to_raw.simulate_undershoot_on_slice(undershoot_parameter, s),
                         image_slices)))


def add_start_of_line_ringing(calibrated_converter):
    # type: (CalibratedConverter) -> CalibratedConverter
    """
    Add *start of line ringing* to a
    :py:class:`~httm.data_structures.calibrated_converter.CalibratedConverter` by calling
    :py:func:`~httm.transformations.calibrated_slices_to_raw.add_start_of_line_ringing_to_slice`
    over each slice.

    :param calibrated_converter: Should have electrons for units for each of its slices
    :type calibrated_converter: :py:class:`~httm.data_structures.calibrated_converter.CalibratedConverter`
    :rtype: :py:class:`~httm.data_structures.calibrated_converter.CalibratedConverter`
    """
    start_of_line_ringing_patterns = load_npz_resource(calibrated_converter.parameters.start_of_line_ringing)
    image_slices = calibrated_converter.slices
    return calibrated_converter._replace(
        slices=tuple(
            calibrated_slices_to_raw.add_start_of_line_ringing_to_slice(start_of_line_ringing, image_slice)
            for (start_of_line_ringing, image_slice) in zip(start_of_line_ringing_patterns, image_slices)))


def add_pattern_noise(calibrated_converter):
    # type: (CalibratedConverter) -> CalibratedConverter
    """
    Add *pattern noise* to a :py:class:`~httm.data_structures.calibrated_converter.CalibratedConverter` by calling
    :py:func:`~httm.transformations.calibrated_slices_to_raw.add_pattern_noise_to_slice` over each slice.

    :param calibrated_converter: Should have electrons for units for each of its slices
    :type calibrated_converter: :py:class:`~httm.data_structures.calibrated_converter.CalibratedConverter`
    :rtype: :py:class:`~httm.data_structures.calibrated_converter.CalibratedConverter`
    """
    pattern_noises = load_npz_resource(calibrated_converter.parameters.pattern_noise)
    image_slices = calibrated_converter.slices
    return calibrated_converter._replace(
        slices=tuple(
            calibrated_slices_to_raw.add_pattern_noise_to_slice(pattern_noise, image_slice)
            for (pattern_noise, image_slice) in zip(pattern_noises, image_slices)))


def convert_electrons_to_adu(calibrated_converter):
    # type: (CalibratedConverter) -> CalibratedConverter
    """
    Converts a :py:class:`~httm.data_structures.calibrated_converter.CalibratedConverter` from having electrons
    to *Analogue to Digital Converter Units* (ADU) by calling
    :py:func:`~httm.transformations.calibrated_slices_to_raw.convert_slice_electrons_to_adu` over each slice.

    :param calibrated_converter: Should have electrons for units for each of its slices
    :type calibrated_converter: :py:class:`~httm.data_structures.calibrated_converter.CalibratedConverter`
    :rtype: :py:class:`~httm.data_structures.calibrated_converter.CalibratedConverter`
    """
    video_scales = calibrated_converter.parameters.video_scales
    image_slices = calibrated_converter.slices
    number_of_exposures = calibrated_converter.parameters.number_of_exposures
    gain_loss = calibrated_converter.parameters.gain_loss
    baseline_adus = calibrated_converter.parameters.baseline_adu
    clip_level_adu = calibrated_converter.parameters.clip_level_adu
    assert len(video_scales) == len(image_slices), "Video scales do not match image slices"
    # noinspection PyProtectedMember
    return calibrated_converter._replace(
        slices=tuple(
            calibrated_slices_to_raw.convert_slice_electrons_to_adu(gain_loss, number_of_exposures, video_scale,
                                                                    baseline_adu, clip_level_adu,
                                                                    image_slice)
            for (video_scale, baseline_adu, image_slice) in zip(video_scales, baseline_adus, image_slices)))
