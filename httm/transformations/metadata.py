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
``httm.transformations.metadata``
=================================

This module contains metadata related to transformation functions.

  - ``electron_flux_transformations`` is metadata describing transformation functions from images in
    electron counts to simulated raw images in *Analogue to Digital Converter Units* (ADU).
  - ``raw_transformations`` is metadata describing transformation functions from raw images in
    *Analogue to Digital Converter Units* (ADU) to calibrated images in electron counts.
"""

from collections import OrderedDict

from .raw_converters_to_calibrated import remove_pattern_noise, convert_adu_to_electrons, remove_baseline, \
    remove_start_of_line_ringing, remove_undershoot, remove_smear
from .electron_flux_converters_to_raw import introduce_smear_rows, add_shot_noise, simulate_blooming, \
    add_readout_noise, simulate_undershoot, simulate_start_of_line_ringing, add_baseline, convert_electrons_to_adu, \
    add_pattern_noise

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
    ('add_pattern_noise', {
        'default': True,
        'documentation': 'Add a fixed *pattern noise* to each slice in the image.',
        'function': add_pattern_noise,
    }),
])

raw_transformations = OrderedDict([
    ('remove_pattern_noise', {
        'default': True,
        'documentation': 'Compensate for a fixed *pattern noise* on each slice of the image.',
        'function': remove_pattern_noise,
    }),
    ('convert_adu_to_electrons', {
        'default': True,
        'documentation': 'Convert the image from having units in '
                         '*Analogue to Digital Converter Units* (ADU) '
                         'to electron counts.',
        'function': convert_adu_to_electrons,
    }),
    ('remove_baseline', {
        'default': True,
        'documentation': 'Average the pixels in the dark columns and subtract '
                         'the result from each pixel in the image.',
        'function': remove_baseline,
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
