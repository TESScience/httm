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
``httm.data_structures.metadata``
=================================

This module contains metadata for use in transformation functions.

  - ``parameters`` is metadata describing various parameters that transformation functions might use.
  - ``transformation_flags`` is metadata describing status flags so that transformations are not accidentally
    run more than once over the same data.
"""

from collections import OrderedDict

from ..transformations.constants import FPE_MAX_ADU

parameters = OrderedDict([
    ('number_of_slices', {
        'type': 'int',
        'documentation': 'The number of slices to use in the transformation, either ``1`` or ``4``.',
        'short_documentation': 'The number of slices used: 1 or 4',
        'default': 4,
        'standard_fits_keyword': 'N_SLICES',
        'forbidden_fits_keywords': [],
        'alternate_fits_keywords': [],
        'required_keyword': False,
    }),
    ('camera_number', {
        'type': 'int',
        'documentation': 'The number of the camera that took the image. '
                         'For real images, the serial number 0-31 of the FPE interface board is used.',
        'short_documentation': 'The number of the camera that took the image.',
        'default': -1,
        'standard_fits_keyword': 'CAMNUM',
        'forbidden_fits_keywords': [],
        'alternate_fits_keywords': [],
        'required_keyword': True,
    }),
    ('ccd_number', {
        'type': 'int',
        'default': -1,
        'documentation': 'The number of the CCD that took the image.',
        'standard_fits_keyword': 'CCDNUM',
        'forbidden_fits_keywords': [],
        'alternate_fits_keywords': ['CCD', 'CROPID'],
        'required_keyword': True,
    }),
    ('number_of_exposures', {
        'type': 'int',
        'documentation': 'The number of frames stacked in the image.',
        'default': 1,
        'standard_fits_keyword': 'N_FRAMES',
        'forbidden_fits_keywords': [],
        'alternate_fits_keywords': ['NREADS'],
        'required_keyword': True,
    }),
    ('video_scales', {
        'type': 'tuple of :py:class:`float` objects, must have one for each slice',
        'documentation': 'The video scaling constants, for converting back and forth between '
                         '*Analogue to Digital Converter Units* (ADU) to electron counts. '
                         'These have units of electrons per ADU.',
        'short_documentation': 'The video scaling constants.',
        'default': (5.5, 5.5, 5.5, 5.5),
        'standard_fits_keyword': ['VSCALE1', 'VSCALE2', 'VSCALE3', 'VSCALE4', ],
        'forbidden_fits_keywords': [],
        'required_keyword': False,
    }),
    ('readout_noise_parameters', {
        'type': 'tuple of :py:class:`float` objects, must have one for each slice',
        'documentation': 'The video readout noise standard deviation in electrons. '
                         'Corresponds to fluctuations in electron counts for completely '
                         'dark pixel data.',
        'short_documentation': 'Video readout noise std in electrons.',
        'default': (9.5, 9.5, 9.5, 9.5),
        'standard_fits_keyword': ['RNOISE1', 'RNOISE2', 'RNOISE3', 'RNOISE4', ],
        'forbidden_fits_keywords': ['READNOIS'],
        'required_keyword': False,
    }),
    ('early_dark_pixel_columns', {
        'type': 'int',
        'documentation': 'Count of columns of pixels that have never traversed the image area '
                         'or frame store, and thus were never exposed to light. '
                         'Read before the image pixels in the row, these '
                         'are where most of the start of line ringing may be seen.',
        'short_documentation': 'The number of dark pixels read BEFORE image.',
        'default': 11,
        'standard_fits_keyword': 'LDRKCLS',
        'forbidden_fits_keywords': [],
        'alternate_fits_keywords': [],
        'required_keyword': False,
    }),
    ('late_dark_pixel_columns', {
        'type': 'int',
        'documentation': 'Count of columns of pixels that have never traversed the image area '
                         'or frame store, and thus were never exposed to light. '
                         'Read after the image pixels in a row.',
        'short_documentation': 'The number of dark pixels read AFTER image.',
        'default': 11,
        'standard_fits_keyword': 'RDRKCLS',
        'forbidden_fits_keywords': [],
        'alternate_fits_keywords': [],
        'required_keyword': False,
    }),
    ('final_dark_pixel_rows', {
        'type': 'int',
        'documentation': 'Count of rows of pixels that have traversed the frame store area, '
                         'but not the image area, and thus were never exposed to light.',
        'short_documentation': '# of rows traversed frame store but not image.',
        'default': 10,
        'standard_fits_keyword': 'TDRKCLS',
        'forbidden_fits_keywords': [],
        'alternate_fits_keywords': [],
        'required_keyword': False,
    }),
    ('smear_rows', {
        'type': 'int',
        'documentation': 'Count of rows of pixels that have traversed the imaging area during '
                         'frame transfer, but have zero exposure to light otherwise. '
                         'These are for estimating the effect of smear on the imaging pixels.',
        'short_documentation': '# rows traversed the frame store with no light.',
        'default': 10,
        'standard_fits_keyword': 'SMRROWS',
        'forbidden_fits_keywords': [],
        'alternate_fits_keywords': [],
        'required_keyword': False,
    }),
    ('random_seed', {
        'type': 'int',
        'documentation': 'The pseudo random number generator seed. '
                         'The default value of ``None`` creates a seed from the system clock.',
        'short_documentation': 'The pseudo random number generator seed',
        'default': None,
        'standard_fits_keyword': 'RNGSEED',
        'forbidden_fits_keywords': [],
        'alternate_fits_keywords': [],
        'required_keyword': False,
    }),
    ('full_well', {
        'type': 'float',
        'documentation': 'The expected maximum number of electrons that a pixel can hold.',
        'short_documentation': 'Max # of electrons a pixel can hold',
        'default': 170000.0,
        'standard_fits_keyword': 'FULLWELL',
        'forbidden_fits_keywords': [],
        'alternate_fits_keywords': [],
        'required_keyword': False,
    }),
    ('blooming_threshold', {
        'type': 'float',
        'documentation': 'The expected maximum number of electrons before a pixel blooms.',
        'short_documentation': 'Max # of electrons before a pixel blooms',
        'default': 140000.0,
        'standard_fits_keyword': 'BLMTHRSH',
        'forbidden_fits_keywords': [],
        'alternate_fits_keywords': [],
        'required_keyword': False,
    }),
    ('gain_loss', {
        'type': 'float',
        'documentation': 'The relative decrease in video gain over the total ADC range. '
                         'This is the parameter of the non-linearity model. '
                         'This is sometimes referred to as *compression* in electrical engineering literature.',
        'short_documentation': "Relative decrease in gain over total ADC range",
        'default': 0.01,
        'standard_fits_keyword': 'GAINLOSS',
        'forbidden_fits_keywords': [],
        'alternate_fits_keywords': [],
        'required_keyword': False,
    }),
    ('undershoot_parameter', {
        'type': 'float',
        'documentation': 'The deficit in a pixel value relative to the value of its '
                         'preceding pixel.  This is a ratio and dimensionless. '
                         'The electronics have a slight memory of the '
                         'signal level which cause the pixel following a bright pixel '
                         'to appear slightly darker that it should.',
        'short_documentation': 'Deficit of pixel relative to preceding',
        'default': 0.0013,
        'standard_fits_keyword': 'UNDRSHUT',
        'forbidden_fits_keywords': [],
        'alternate_fits_keywords': [],
        'required_keyword': False,
    }),
    ('single_frame_baseline_adus', {
        'type': 'float',
        'documentation': 'The mean ADU for a pixel with zero electrons for a single '
                         'simulated frame exposure, per slice.',
        'short_documentation': 'Mean ADU for pixel for single frame.',
        'default': (6000.0, 6000.0, 6000.0, 6000.0,),
        'standard_fits_keyword': ['BASEADU1', 'BASEADU2', 'BASEADU3', 'BASEADU4', ],
        'forbidden_fits_keywords': [],
        'alternate_fits_keywords': [],
        'required_keyword': False,
    }),
    ('single_frame_baseline_adu_drift_term', {
        'type': 'float',
        'documentation': 'Standard deviation of a random number added to the single frame baseline adu parameter '
                         'per simulated frame (same for all slices).',
        'short_documentation': 'ADU STD for a pixel for a simulated frame',
        'default': 0.0,
        'standard_fits_keyword': 'DRIFTADU',
        'forbidden_fits_keywords': [],
        'alternate_fits_keywords': [],
        'required_keyword': False,
    }),
    ('smear_ratio', {
        'type': 'float',
        'documentation': 'The time that a charge packet spends in transit through '
                         'each imaging pixel that it does not nominally belong to, relative '
                         'to the time it spends in the pixel it does nominally belong to. '
                         'Used for simulating smear rows.',
        'short_documentation': 'Ratio used for simulating smear rows',
        'default': 4.84836e-06,
        'standard_fits_keyword': 'SMRRATIO',
        'forbidden_fits_keywords': [],
        'alternate_fits_keywords': [],
        'required_keyword': False,
    }),
    ('clip_level_adu', {
        'type': 'int',
        'documentation': 'The level in ADU where the CCD or the electronics will clip the video. '
                         'The default is the maximum the *Analogue to Digital Converter* (ADC) can deliver.',
        'short_documentation': 'Level where video is clipped in ADU',
        'default': FPE_MAX_ADU,
        'standard_fits_keyword': 'CLIP_ADU',
        'forbidden_fits_keywords': [],
        'alternate_fits_keywords': [],
        'required_keyword': False,
    }),
    ('start_of_line_ringing', {
        'type': ':py:class:`str` or :py:class:`file`',
        'documentation': 'A vector to be read from an ``npz`` file, to be added to '
                         'each row in of a slice, representing the repeatable '
                         'change in the video baseline caused by the disturbance '
                         'in the data acquisition rhythm between *rows*. '
                         'Units of the array are electrons.',
        'short_documentation': 'Start of line ringing',
        'default': 'built-in default_start_of_line_ringing.npz',
        'standard_fits_keyword': 'SOLRING',
        'forbidden_fits_keywords': [],
        'alternate_fits_keywords': [],
        'required_keyword': False,
    }),
    ('pattern_noise', {
        'type': ':py:class:`str` or :py:class:`file`',
        'documentation': 'A matrix to be read from an ``npz`` file, '
                         'representing the repeatable change in the video baseline caused by the disturbance '
                         'in the data acquisition rhythm between *frames*. '
                         'Units of the matrix are electrons.',
        'short_documentation': 'Pattern noise',
        'default': 'built-in default_pattern_noise.npz',
        'standard_fits_keyword': 'PATNOISE',
        'forbidden_fits_keywords': [],
        'alternate_fits_keywords': [],
        'required_keyword': False,
    }),
])

transformation_flags = OrderedDict([
    ('smear_rows_present', {
        'type': 'bool',
        'documentation': 'Flag indicating whether there is data in the smear rows.',
        'short_documentation': 'Smear rows present?',
        'standard_fits_keyword': 'SMRPRES',
        'forbidden_fits_keywords': [],
        'alternate_fits_keywords': [],
        'required_keyword': False,
    }),
    ('shot_noise_present', {
        'type': 'bool',
        'documentation': 'Flag indicating whether *shot noise* is present.',
        'short_documentation': 'Shot noise present?',
        'standard_fits_keyword': 'SHNOISEP',
        'forbidden_fits_keywords': [],
        'alternate_fits_keywords': [],
        'required_keyword': False,
    }),
    ('blooming_present', {
        'type': 'bool',
        'documentation': 'Flag indicating whether *blooming* has been simulated.',
        'short_documentation': 'Blooming present?',
        'standard_fits_keyword': 'BLOOMP',
        'forbidden_fits_keywords': [],
        'alternate_fits_keywords': [],
        'required_keyword': False,
    }),
    ('readout_noise_present', {
        'type': 'bool',
        'documentation': 'Flag indicating whether *readout noise* is present.',
        'short_documentation': 'Readout noise present?',
        'standard_fits_keyword': 'RDNOISEP',
        'forbidden_fits_keywords': [],
        'alternate_fits_keywords': [],
        'required_keyword': False,
    }),
    ('undershoot_present', {
        'type': 'bool',
        'documentation': 'Flag indicating whether *undershoot* is present or otherwise compensated for.',
        'short_documentation': 'Undershoot present?',
        'standard_fits_keyword': 'UNDRSP',
        'forbidden_fits_keywords': [],
        'alternate_fits_keywords': [],
        'required_keyword': False,
    }),
    ('start_of_line_ringing_present', {
        'type': 'bool',
        'documentation': 'Flag indicating whether *start of line ringing* is present or otherwise compensated for.',
        'short_documentation': 'Start of line ringing present?',
        'standard_fits_keyword': 'SOLRP',
        'forbidden_fits_keywords': [],
        'alternate_fits_keywords': [],
        'required_keyword': False,
    }),
    ('pattern_noise_present', {
        'type': 'bool',
        'documentation': 'Flag indicating whether *pattern noise* is present or otherwise compensated for.',
        'short_documentation': 'Pattern noise present?',
        'standard_fits_keyword': 'PTNOISEP',
        'forbidden_fits_keywords': [],
        'alternate_fits_keywords': [],
        'required_keyword': False,
    }),
    ('baseline_present', {
        'type': 'bool',
        'documentation': 'Flag indicating whether a *baseline electron count* is present or otherwise compensated for.',
        'short_documentation': 'Baseline present?',
        'standard_fits_keyword': 'BASELN',
        'forbidden_fits_keywords': [],
        'alternate_fits_keywords': [],
        'required_keyword': False,
    }),
    ('in_adu', {
        'type': 'bool',
        'documentation': 'Flag indicating whether the data is in *Analogue to Digital Converter Units* '
                         'or otherwise in electron counts.',
        'short_documentation': 'Image in ADU? (o/w in electrons)',
        'standard_fits_keyword': 'ADU',
        'forbidden_fits_keywords': [],
        'alternate_fits_keywords': [],
        'required_keyword': False,
    }),
])
