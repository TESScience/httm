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
``httm.transformations.electron_flux_converters_to_raw``
========================================================

Transformation functions for processing
:py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter` objects so that
they are suitable  for writing to a simulated raw FITS file.

"""
from collections import OrderedDict

from .common import derive_transformation_function_list
from .electron_flux_slices_to_raw import introduce_smear_rows_to_slice, add_shot_noise_to_slice, \
    simulate_blooming_on_slice, add_baseline_to_slice, add_readout_noise_to_slice, simulate_undershoot_on_slice, \
    simulate_start_of_line_ringing_to_slice, add_pattern_noise_to_slice, convert_slice_electrons_to_adu
from ..data_structures.electron_flux_converter import SingleCCDElectronFluxConverter
from ..resource_utilities import load_npz_resource


def introduce_smear_rows(electron_flux_converter):
    # type: (SingleCCDElectronFluxConverter) -> SingleCCDElectronFluxConverter
    """
    Add *smear rows* to a
    :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`.

    Calls
    :py:func:`~httm.transformations.electron_flux_slices_to_raw.introduce_smear_rows_to_slice`
    over each slice.

    :param electron_flux_converter: Should have electrons for units for each of its slices
    :type electron_flux_converter: \
    :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`
    :rtype: :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`
    """
    assert electron_flux_converter.flags.smear_rows_present is False, "Smear rows must not be flagged as present"
    smear_ratio = electron_flux_converter.parameters.smear_ratio
    smear_rows = electron_flux_converter.parameters.smear_rows
    final_dark_pixel_rows = electron_flux_converter.parameters.final_dark_pixel_rows
    late_dark_pixel_columns = electron_flux_converter.parameters.late_dark_pixel_columns
    early_dark_pixel_columns = electron_flux_converter.parameters.early_dark_pixel_columns
    image_slices = electron_flux_converter.slices
    # noinspection PyProtectedMember
    return electron_flux_converter._replace(
        slices=tuple(introduce_smear_rows_to_slice(smear_ratio, early_dark_pixel_columns,
                                                   late_dark_pixel_columns,
                                                   final_dark_pixel_rows, smear_rows, image_slice)
                     for image_slice in image_slices),
        flags=electron_flux_converter.flags._replace(smear_rows_present=True))


def add_shot_noise(electron_flux_converter):
    # type: (SingleCCDElectronFluxConverter) -> SingleCCDElectronFluxConverter
    """
    Add *shot noise* to each pixel in each slice in a
    :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`.

    Calls :py:func:`~httm.transformations.electron_flux_slices_to_raw.add_shot_noise_to_slice`
    over each slice.

    :param electron_flux_converter: Should have electrons for units for each of its slices
    :type electron_flux_converter: \
    :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`
    :rtype: :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`
    """
    assert electron_flux_converter.flags.shot_noise_present is False, "Shot noise must not be flagged as present"
    image_slices = electron_flux_converter.slices
    # noinspection PyProtectedMember
    return electron_flux_converter._replace(
        slices=tuple(add_shot_noise_to_slice(image_slice) for image_slice in image_slices),
        flags=electron_flux_converter.flags._replace(shot_noise_present=True))


def simulate_blooming(electron_flux_converter):
    # type: (SingleCCDElectronFluxConverter) -> SingleCCDElectronFluxConverter
    """
    Simulate *blooming* on for each column for each slice in a
    :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`.

    Calls
    :py:func:`~httm.transformations.electron_flux_slices_to_raw.simulate_blooming_on_slice`
    over each slice.

    :param electron_flux_converter: Should have electrons for units for each of its slices
    :type electron_flux_converter: \
    :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`
    :rtype: :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`
    """
    assert electron_flux_converter.flags.blooming_present is False, "Blooming must not be flagged as present"
    full_well = electron_flux_converter.parameters.full_well
    blooming_threshold = electron_flux_converter.parameters.blooming_threshold
    number_of_exposures = electron_flux_converter.parameters.number_of_exposures
    image_slices = electron_flux_converter.slices
    # noinspection PyProtectedMember
    return electron_flux_converter._replace(
        slices=tuple(simulate_blooming_on_slice(full_well, blooming_threshold, number_of_exposures, image_slice)
                     for image_slice in image_slices),
        flags=electron_flux_converter.flags._replace(blooming_present=True))


def add_baseline(electron_flux_converter):
    # type: (SingleCCDElectronFluxConverter) -> SingleCCDElectronFluxConverter
    """
    Add a random scalar *baseline electron count* to a
    :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter` for
    each :py:class:`~httm.data_structures.common.Slice`.

    Calls
    :py:func:`~httm.transformations.electron_flux_slices_to_raw.add_baseline_to_slice`
    over each slice.

    :param electron_flux_converter: Should have electrons for units for each of its slices
    :type electron_flux_converter: \
    :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`
    :rtype: :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`
    """
    assert electron_flux_converter.flags.baseline_present is False, "Baseline must not be flagged as present"
    image_slices = electron_flux_converter.slices
    single_frame_baseline_adus = electron_flux_converter.parameters.single_frame_baseline_adus
    assert len(single_frame_baseline_adus) >= len(image_slices), \
        "There should be at least as many Baseline ADU values as slices"
    single_frame_baseline_adu_drift_term = electron_flux_converter.parameters.single_frame_baseline_adu_drift_term
    number_of_exposures = electron_flux_converter.parameters.number_of_exposures
    video_scales = electron_flux_converter.parameters.video_scales
    assert len(video_scales) >= len(image_slices), "There should be at least as many video scales as slices"
    # noinspection PyProtectedMember
    return electron_flux_converter._replace(
        slices=tuple(add_baseline_to_slice(single_frame_baseline_adu, single_frame_baseline_adu_drift_term,
                                           number_of_exposures, video_scale, image_slice)
                     for (single_frame_baseline_adu, video_scale, image_slice)
                     in zip(single_frame_baseline_adus, video_scales, image_slices)),
        flags=electron_flux_converter.flags._replace(baseline_present=True))


def add_readout_noise(electron_flux_converter):
    # type: (SingleCCDElectronFluxConverter) -> SingleCCDElectronFluxConverter
    """
    Add *readout noise* to each pixel in each slice in a
    :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`.

    Calls
    :py:func:`~httm.transformations.electron_flux_slices_to_raw.add_readout_noise_to_slice`
    over each slice.

    :param electron_flux_converter: Should have electrons for units for each of its slices
    :type electron_flux_converter: \
    :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`
    :rtype: :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`
    """
    assert electron_flux_converter.flags.readout_noise_present is False, "Readout noise must not be flagged as present"
    readout_noise_parameters = electron_flux_converter.parameters.readout_noise_parameters
    image_slices = electron_flux_converter.slices
    number_of_exposures = electron_flux_converter.parameters.number_of_exposures
    # noinspection PyProtectedMember
    return electron_flux_converter._replace(
        slices=tuple(add_readout_noise_to_slice(readout_noise_parameter, number_of_exposures, image_slice)
                     for (readout_noise_parameter, image_slice) in zip(readout_noise_parameters, image_slices)),
        flags=electron_flux_converter.flags._replace(readout_noise_present=True))


def simulate_undershoot(electron_flux_converter):
    # type: (SingleCCDElectronFluxConverter) -> SingleCCDElectronFluxConverter
    """
    Simulate *undershoot* on each row of each slice in a
    :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`.

    Calls
    :py:func:`~httm.transformations.electron_flux_slices_to_raw.simulate_undershoot_on_slice`
    over each slice.

    :param electron_flux_converter: Should have electrons for units for each of its slices
    :type electron_flux_converter: \
    :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`
    :rtype: :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`
    """
    assert electron_flux_converter.flags.undershoot_present is False, "Undershoot must not be flagged as present"
    undershoot_parameter = electron_flux_converter.parameters.undershoot_parameter
    image_slices = electron_flux_converter.slices
    # noinspection PyProtectedMember
    return electron_flux_converter._replace(
        slices=tuple(simulate_undershoot_on_slice(undershoot_parameter, image_slice) for image_slice in image_slices),
        flags=electron_flux_converter.flags._replace(undershoot_present=True))


def simulate_start_of_line_ringing(electron_flux_converter):
    # type: (SingleCCDElectronFluxConverter) -> SingleCCDElectronFluxConverter
    """
    Simulate *start of line ringing* on each row of each slice in a
    :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`.

    Calls
    :py:func:`~httm.transformations.electron_flux_slices_to_raw.simulate_start_of_line_ringing_to_slice`
    over each slice.

    :param electron_flux_converter: Should have electrons for units for each of its slices
    :type electron_flux_converter: \
    :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`
    :rtype: :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`
    """
    assert electron_flux_converter.flags.start_of_line_ringing_present is False, \
        "Start of line ringing must not be flagged as present"
    start_of_line_ringing_patterns = load_npz_resource(electron_flux_converter.parameters.start_of_line_ringing)
    image_slices = electron_flux_converter.slices
    # noinspection PyProtectedMember
    return electron_flux_converter._replace(
        slices=tuple(simulate_start_of_line_ringing_to_slice(start_of_line_ringing, image_slice)
                     for (start_of_line_ringing, image_slice) in zip(start_of_line_ringing_patterns, image_slices)),
        flags=electron_flux_converter.flags._replace(start_of_line_ringing_present=True))


def add_pattern_noise(electron_flux_converter):
    # type: (SingleCCDElectronFluxConverter) -> SingleCCDElectronFluxConverter
    """
    Add *pattern noise* to each slice in a
    :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`.

    Calls
    :py:func:`~httm.transformations.electron_flux_slices_to_raw.add_pattern_noise_to_slice` over each slice.

    :param electron_flux_converter: Should have electrons for units for each of its slices
    :type electron_flux_converter: \
    :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`
    :rtype: :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`
    """
    assert electron_flux_converter.flags.pattern_noise_present is False, "Pattern noise must not be flagged as present"
    pattern_noises = load_npz_resource(electron_flux_converter.parameters.pattern_noise)
    image_slices = electron_flux_converter.slices
    # noinspection PyProtectedMember
    return electron_flux_converter._replace(
        slices=tuple(add_pattern_noise_to_slice(pattern_noise, image_slice)
                     for (pattern_noise, image_slice) in zip(pattern_noises, image_slices)),
        flags=electron_flux_converter.flags._replace(pattern_noise_present=True))


def convert_electrons_to_adu(electron_flux_converter):
    # type: (SingleCCDElectronFluxConverter) -> SingleCCDElectronFluxConverter
    """
    Converts a :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`
    from having electrons to *Analogue to Digital Converter Units* (ADU).

    Calls
    :py:func:`~httm.transformations.electron_flux_slices_to_raw.convert_slice_electrons_to_adu` over each slice.

    :param electron_flux_converter: Should have electrons for units for each of its slices
    :type electron_flux_converter: \
    :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`
    :rtype: :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`
    """
    assert electron_flux_converter.flags.in_adu is False, \
        "Image must not be in Analogue to Digital Converter Units (ADU)"
    video_scales = electron_flux_converter.parameters.video_scales
    image_slices = electron_flux_converter.slices
    number_of_exposures = electron_flux_converter.parameters.number_of_exposures
    gain_loss = electron_flux_converter.parameters.gain_loss
    clip_level_adu = electron_flux_converter.parameters.clip_level_adu
    assert len(video_scales) >= len(image_slices), \
        "There should be at least as many video scales as there are slices"
    # noinspection PyProtectedMember
    return electron_flux_converter._replace(
        slices=tuple(convert_slice_electrons_to_adu(gain_loss, number_of_exposures, video_scale,
                                                    clip_level_adu, image_slice)
                     for (video_scale, image_slice) in zip(video_scales, image_slices)),
        flags=electron_flux_converter.flags._replace(in_adu=True))


electron_flux_transformations = OrderedDict([
    ('introduce_smear_rows', {
        'default': True,
        'documentation': 'Introduce *smear rows* to each slice of the image.',
        'function': introduce_smear_rows,
    }),
    ('add_shot_noise', {
        'default': True,
        'documentation': 'Add *shot noise* to each pixel in each slice of the image.',
        'function': add_shot_noise,
    }),
    ('simulate_blooming', {
        'default': True,
        'documentation': 'Simulate *blooming* on for each column for each slice of the image.',
        'function': simulate_blooming,
    }),
    ('add_readout_noise', {
        'default': True,
        'documentation': 'Add *readout noise* to each pixel in each slice of the image.',
        'function': add_readout_noise,
    }),
    ('simulate_undershoot', {
        'default': True,
        'documentation': 'Simulate *undershoot* on each row of each slice in the image.',
        'function': simulate_undershoot,
    }),
    ('simulate_start_of_line_ringing', {
        'default': True,
        'documentation': 'Simulate *start of line ringing* on each row of each slice in the image.',
        'function': simulate_start_of_line_ringing,
    }),
    ('add_pattern_noise', {
        'default': True,
        'documentation': 'Add a fixed *pattern noise* to each slice in the image.',
        'function': add_pattern_noise,
    }),
    ('add_baseline', {
        'default': True,
        'documentation': 'Add a *baseline electron count* to each slice in the image.',
        'function': add_baseline,
    }),
    ('convert_electrons_to_adu', {
        'default': True,
        'documentation': 'Convert the image from having pixel units in electron counts to '
                         '*Analogue to Digital Converter Units* (ADU).',
        'function': convert_electrons_to_adu,
    }),
])


def transform_electron_flux_converter(single_ccd_electron_flux_converter,
                                      transformation_settings=None):
    # type: (SingleCCDElectronFluxConverter, object) -> SingleCCDElectronFluxConverter
    """
    Take a :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter` and run specified
    transformations over it.

    :param single_ccd_electron_flux_converter: A \
    :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter` to run a series of \
    transformations over
    :type single_ccd_electron_flux_converter: \
    :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`
    :param transformation_settings: An object specifying which transformations to run; if not specified defaults are \
    used
    :type transformation_settings: object
    :rtype: :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`
    """
    from functools import reduce
    import numpy.random
    random_seed = single_ccd_electron_flux_converter.parameters.random_seed
    numpy.random.seed(random_seed if random_seed is not -1 else None)
    return reduce(
        lambda converter, transformation_function:
        transformation_function(converter),
        derive_transformation_function_list(
            transformation_settings,
            OrderedDict((key, electron_flux_transformations[key]['default'])
                        for key in electron_flux_transformations.keys()),
            {key: electron_flux_transformations[key]['function']
             for key in electron_flux_transformations.keys()}),
        single_ccd_electron_flux_converter)
