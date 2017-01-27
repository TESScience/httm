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
``httm.transformations.raw_converters_to_calibrated``
=====================================================

Transformation functions for processing
:py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter` objects so that
they are suitable for writing to a calibrated FITS file.

"""
from collections import OrderedDict

from .common import derive_transformation_function_list
from .raw_slices_to_calibrated import convert_slice_adu_to_electrons, remove_pattern_noise_from_slice, \
    remove_undershoot_from_slice, remove_smear_from_slice, remove_baseline_from_slice
from ..data_structures.raw_converter import SingleCCDRawConverter
from ..resource_utilities import load_npz_resource


def convert_adu_to_electrons(raw_converter):
    # type: (SingleCCDRawConverter) -> SingleCCDRawConverter
    """
    Converts a :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter` from
    having *Analogue to Digital Converter Units* (ADU) to estimated electron counts by calling
    :py:func:`~httm.transformations.raw_slices_to_calibrated.convert_slice_adu_to_electrons` over each slice.

    :param raw_converter: A :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter` which should \
    have electrons for units for each of its slices
    :type raw_converter: :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter`
    :rtype: :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter`
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
        flags=raw_converter.flags._replace(in_adu=True))


def remove_baseline(raw_converter):
    # type: (SingleCCDRawConverter) -> SingleCCDRawConverter
    """
    This function estimates *baseline* from the *dark pixels* for each slice in a
    :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter`
    and compensates for this effect. Calls
    :py:func:`~httm.transformations.raw_slices_to_calibrated.remove_baseline_from_slice` over each slice.

    Note that if you do not remove baseline using this routine prior to removing undershoot, then artifacts
    are introduced at the early edge of a row.

    :param raw_converter: A :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter` which should \
    have *Analogue to Digital Converter Units* (ADU) for units for each of its slices
    :type raw_converter: :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter`
    :rtype: :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter`
    """
    assert raw_converter.flags.baseline_present, "Baseline must be flagged as present"
    image_slices = raw_converter.slices
    early_dark_pixel_columns = raw_converter.parameters.early_dark_pixel_columns
    late_dark_pixel_columns = raw_converter.parameters.late_dark_pixel_columns
    # noinspection PyProtectedMember
    return raw_converter._replace(
        slices=tuple(remove_baseline_from_slice(early_dark_pixel_columns, late_dark_pixel_columns, image_slice)
                     for image_slice in image_slices),
        flags=raw_converter.flags._replace(baseline_present=False))


def remove_pattern_noise(raw_converter):
    # type: (SingleCCDRawConverter) -> SingleCCDRawConverter
    """
    Compensates for a fixed pattern noise, that varies from slice to slice, on a
    :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter`
    by calling :py:func:`~httm.transformations.raw_slices_to_calibrated.remove_pattern_noise_from_slice`
    over each slice.

    :param raw_converter: A :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter` which should \
    have electrons for units for each of its slices
    :type raw_converter: :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter`
    :rtype: :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter`
    """
    assert raw_converter.flags.pattern_noise_present, "Pattern noise must be flagged as present"
    pattern_noises = load_npz_resource(raw_converter.parameters.pattern_noise)
    image_slices = raw_converter.slices
    assert len(pattern_noises) >= len(image_slices), "There should be at least as many noise patterns as slices"
    # noinspection PyProtectedMember
    return raw_converter._replace(
        slices=tuple(remove_pattern_noise_from_slice(pattern_noise, image_slice)
                     for (pattern_noise, image_slice) in zip(pattern_noises, image_slices)),
        flags=raw_converter.flags._replace(pattern_noise_present=False))


def remove_start_of_line_ringing(raw_converter):
    # type: (SingleCCDRawConverter) -> SingleCCDRawConverter
    """
    Compensates for *start of line ringing* on each row in a
    :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter`
    by calling :py:func:`~httm.transformations.raw_slices_to_calibrated.remove_start_of_line_ringing_from_slice`
    over each slice.

    :param raw_converter: A :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter` which should \
    have electrons for units for each of its slices
    :type raw_converter: :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter`
    :rtype: :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter`
    """
    assert raw_converter.flags.start_of_line_ringing_present, "Start of line ringing must be flagged as present"
    final_dark_pixel_rows = raw_converter.parameters.final_dark_pixel_rows
    image_slices = raw_converter.slices
    # noinspection PyProtectedMember
    return raw_converter._replace(
        slices=tuple(remove_pattern_noise_from_slice(final_dark_pixel_rows, image_slice)
                     for image_slice in image_slices),
        flags=raw_converter.flags._replace(start_of_line_ringing_present=False))


def remove_undershoot(raw_converter):
    # type: (SingleCCDRawConverter) -> SingleCCDRawConverter
    """
    Removes *undershoot* from each row in a
    :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter`
    by calling :py:func:`~httm.transformations.raw_slices_to_calibrated.remove_undershoot_from_slice`
    over each slice.

    :param raw_converter: A :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter` which should \
    have electrons for units for each of its slices
    :type raw_converter: :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter`
    :rtype: :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter`
    """
    assert raw_converter.flags.undershoot_present, "Undershoot must be flagged as present"
    assert raw_converter.flags.baseline_present is False, "Baseline should be removed before removing undershoot"

    undershoot_parameter = raw_converter.parameters.undershoot_parameter
    image_slices = raw_converter.slices
    # noinspection PyProtectedMember
    return raw_converter._replace(
        slices=tuple(remove_undershoot_from_slice(undershoot_parameter, image_slice)
                     for image_slice in image_slices),
        flags=raw_converter.flags._replace(undershoot_present=False))


def remove_smear(raw_converter):
    # type: (SingleCCDRawConverter) -> SingleCCDRawConverter
    """
    Removes *smear* and zeroes the *smear rows* in a
    :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter`
    by calling :py:func:`~httm.transformations.raw_slices_to_calibrated.remove_smear_from_slice`
    over each slice.

    :param raw_converter: A :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter` which should \
    have electrons for units for each of its slices
    :type raw_converter: :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter`
    :rtype: :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter`
    """
    assert raw_converter.flags.smear_rows_present, "Smear rows must be flagged as present"
    final_dark_pixel_rows = raw_converter.parameters.final_dark_pixel_rows
    smear_rows = raw_converter.parameters.smear_rows
    late_dark_pixel_columns = raw_converter.parameters.late_dark_pixel_columns
    early_dark_pixel_columns = raw_converter.parameters.early_dark_pixel_columns
    image_slices = raw_converter.slices
    # noinspection PyProtectedMember
    return raw_converter._replace(
        slices=tuple(remove_smear_from_slice(early_dark_pixel_columns, late_dark_pixel_columns,
                                             final_dark_pixel_rows, smear_rows, image_slice)
                     for image_slice in image_slices),
        flags=raw_converter.flags._replace(smear_rows_present=False))


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
        'documentation': 'Average the pixels in the dark columns and subtract ' +
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


def transform_raw_converter(raw_converter, transformation_settings=None):
    # type: (SingleCCDRawConverter, object) -> SingleCCDRawConverter
    """
    Take a :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter` and run specified transformations
    over it.

    :param raw_converter: A :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter` to run a series of \
    transformations over
    :type raw_converter: :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter`
    :param transformation_settings: An object specifying which transformations to run; if not specified defaults are \
    used
    :type transformation_settings: object
    :rtype: :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter`
    """
    from functools import reduce
    return reduce(
        lambda converter, transformation_function:
        transformation_function(converter),
        derive_transformation_function_list(transformation_settings,
                                            OrderedDict((key, raw_transformations[key]['default'])
                                                        for key in raw_transformations.keys()),
                                            {key: raw_transformations[key]['function']
                                             for key in raw_transformations.keys()}),
        raw_converter)
