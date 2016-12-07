"""
``httm.data_structures.metadata``
===================================

This module contains metadata for use in transformation functions.

  - `parameters` is metadata describing various parameters that transformation functions might use.
  - `transformation_flags` is metadata describing status flags so that transformations are not accidentally
    run more than once over the same data.
"""

from collections import OrderedDict
from ..transformations.constants import FPE_MAX_ADU

parameters = OrderedDict([
    ('number_of_slices', {
        'type': 'int',
        'documentation': 'The number of slices to use in the transformation, either ``1`` or ``4``',
        'default': 4,
        'standard_fits_keyword': 'N_SLICES',
        'required_keyword': False,
    }),
    ('camera_number', {
        'type': 'int',
        'documentation': 'The number of the camera that took the image.',
        'default': 0,
        'standard_fits_keyword': 'CAMNUM',
        'required_keyword': True,
    }),
    ('ccd_number', {
        'type': 'int',
        'default': 0,
        'documentation': 'The number of the CCD that took the image.',
        'standard_fits_keyword': 'CCDNUM',
        'required_keyword': True,
    }),
    ('number_of_exposures', {
        'type': 'int',
        'documentation': 'The number of frames stacked in the image.',
        'default': 1,
        'standard_fits_keyword': 'N_FRAMES',
        'alternate_fits_keywords': ['NREADS'],
        'required_keyword': True,
    }),
    ('video_scales', {
        'type': 'tuple of :py:class:`float` objects, must have one for each slice',
        'documentation': 'The video scaling constants, for converting back and forth between '
                         '*Analogue to Digital Converter Units* (ADU) to electron counts. '
                         'These have units of electrons per ADU.',
        'default': (5.5, 5.5, 5.5, 5.5),
        'standard_fits_keyword': ['VSCALE1', 'VSCALE2', 'VSCALE3', 'VSCALE4', ],
        'required_keyword': False,
    }),
    ('readout_noise_parameters', {
        'type': 'tuple of :py:class:`float` objects, must have one for each slice',
        'documentation': 'The video readout noise standard deviation in electrons. '
                         'Corresponds to fluctuations in electron counts for completely '
                         'dark pixel data.',
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
                         'are where most of the start of line ringing may be seen. ',
        'default': 11,
        'standard_fits_keyword': 'LDRKCLS',
        'required_keyword': False,
    }),
    ('late_dark_pixel_columns', {
        'type': 'int',
        'documentation': 'Count of columns of pixels that have never traversed the image area '
                         'or frame store, and thus were never exposed to light. '
                         'Read after the image pixels in a row. ',
        'default': 11,
        'standard_fits_keyword': 'RDRKCLS',
        'required_keyword': False,
    }),
    ('final_dark_pixel_rows', {
        'type': 'int',
        'documentation': 'Count of rows of pixels that have traversed the frame store area, '
                         'but not the image area, and thus were never exposed to light. ',
        'default': 10,
        'standard_fits_keyword': 'TDRKCLS',
        'required_keyword': False,
    }),
    ('smear_rows', {
        'type': 'int',
        'documentation': 'Count of rows of pixels that have traversed the imaging area during '
                         'frame transfer, but have zero exposure to light otherwise. '
                         'These are for estimating the effect of smear on the imaging pixels.',
        'default': 10,
        'standard_fits_keyword': 'SMRROWS',
        'required_keyword': False,
    }),
    ('random_seed', {
        'type': 'int',
        'documentation': 'The seed value to hand to the random number generator',
        'default': None,
        'standard_fits_keyword': 'RNGSEED',
        'required_keyword': False,
    }),
    ('full_well', {
        'type': 'float',
        'documentation': 'The expected maximum number of electrons that a pixel can hold.',
        'default': 170000.0,
        'standard_fits_keyword': 'FULLWELL',
        'required_keyword': False,
    }),
    ('blooming_threshold', {
        'type': 'float',
        'documentation': 'The expected maximum number of electrons before a pixel blooms.',
        'default': 140000.0,
        'standard_fits_keyword': 'BLMTHRSH',
        'required_keyword': False,
    }),
    ('gain_loss', {
        'type': 'float',
        'documentation': 'The relative decrease in video gain over the total ADC range. '
                         'This is the parameter of our non-linearity model. '
                         'This is sometimes referred to as *compression* in the electrical engineering literature.',
        'default': 0.01,
        'standard_fits_keyword': 'GAINLOSS',
        'required_keyword': False,
    }),
    ('undershoot_parameter', {
        'type': 'float',
        'documentation': 'The deficit in a pixel value relative to the value of its '
                         'preceding pixel. The electronics have a slight memory of the '
                         'signal level which cause the pixel following a bright pixel '
                         'to appear slightly darker that it should.',
        'default': 0.0013,
        'standard_fits_keyword': 'UNDRSHUT',
        'required_keyword': False,
    }),
    ('single_frame_baseline_adus', {
        'type': 'float',
        'documentation': 'The mean ADU for a pixel with zero electrons for a single frame exposure, per slice.',
        'default': (6000.0, 6000.0, 6000.0, 6000.0,),
        'standard_fits_keyword': ['BASEADU1', 'BASEADU2', 'BASEADU3', 'BASEADU4'],
        'required_keyword': False,
    }),
    ('single_frame_baseline_adu_drift_term', {
        'type': 'float',
        'documentation': 'Standard deviation of a random number added to the single_frame_baseline_adu '
                         'per simulated frame, to stress the baseline determination code.',
        'default': 0.0,
        'standard_fits_keyword': 'DRIFTADU',
        'required_keyword': False,
    }),
    ('smear_ratio', {
        'type': 'float',
        'documentation': 'The time that a charge packet spends in transit through '
                         "each imaging pixel that it doesn't nominally belong to, relative "
                         'to the time it spends in the pixel it does nominally belong to. '
                         'Derived from the sequencer program. '
                         'The default is derived from ``Hemiola.fpe``.',
        'default': 4.84836e-06,
        'standard_fits_keyword': 'SMRRATIO',
        'required_keyword': False,
    }),
    ('clip_level_adu', {
        'type': 'int',
        'documentation': 'The level in ADU where the CCD or the electronics will '
                         'clip the video. The default is the maximum the *Analogue to Digital Converter* (ADC) '
                         'can deliver.',
        'default': FPE_MAX_ADU,
        'standard_fits_keyword': 'CLIP_ADU',
        'required_keyword': False,
    }),
    ('start_of_line_ringing', {
        'type': ':py:class:`str` or :py:class:`file`',
        'documentation': 'A vector to be read from an ``npz`` file, to be added to '
                         'each row in of a slice, representing the repeatable '
                         'change in the video baseline caused by the disturbance '
                         'in the data acquisition rhythm between *rows*. '
                         'Units of the array are electrons.',
        'default': ':httm:/data/default_start_of_line_ringing.npz',
        'standard_fits_keyword': 'SOLRING',
        'required_keyword': False,
    }),
    ('pattern_noise', {
        'type': ':py:class:`str` or :py:class:`file`',
        'documentation': 'A matrix to be read from an ``npz`` file, to be added to the pixel data '
                         'array for each slice, representing the repeatable '
                         'change in the video baseline caused by the disturbance '
                         'in the data acquisition rhythm between *frames*. '
                         'Units of the matrix are electrons.',
        'default': ':httm:/data/default_pattern_noise.npz',
        'standard_fits_keyword': 'PATNOISE',
        'required_keyword': False,
    })
])

transformation_flags = OrderedDict([
    ('smear_rows_present', {
        'type': 'bool',
        'documentation': 'Indicates whether there is data in the smear rows.',
        'standard_fits_keyword': 'SMRPRES',
        'required_keyword': False,
    }),
    ('shot_noise_present', {
        'type': 'bool',
        'documentation': 'Indicates whether *shot noise* is present.',
        'standard_fits_keyword': 'SHNOISEP',
        'required_keyword': False,
    }),
    ('blooming_present', {
        'type': 'bool',
        'documentation': 'Indicates whether *blooming* has been simulated.',
        'standard_fits_keyword': 'BLOOMP',
        'required_keyword': False,
    }),
    ('readout_noise_present', {
        'type': 'bool',
        'documentation': 'Indicates whether *readout noise* is present.',
        'standard_fits_keyword': 'RDNOISEP',
        'required_keyword': False,
    }),
    ('undershoot_present', {
        'type': 'bool',
        'documentation': 'Indicates whether *undershoot* is present or otherwise compensated for.',
        'standard_fits_keyword': 'UNDRSP',
        'required_keyword': False,
    }),
    ('start_of_line_ringing_present', {
        'type': 'bool',
        'documentation': 'Indicates whether *start of line ringing* is present or otherwise compensated for.',
        'standard_fits_keyword': 'SOLRP',
        'required_keyword': False,
    }),
    ('pattern_noise_present', {
        'type': 'bool',
        'documentation': 'Indicates whether *pattern noise* is present or otherwise compensated for.',
        'standard_fits_keyword': 'PTNOISEP',
        'required_keyword': False,
    }),
    ('baseline_present', {
        'type': 'bool',
        'documentation': 'Indicates whether a *baseline electron count* is present or otherwise compensated for.',
        'standard_fits_keyword': 'BASELN',
        'required_keyword': False,
    }),
    ('in_adu', {
        'type': 'bool',
        'documentation': 'Indicates whether the data is in *Analogue to Digital Converter Units* '
                         'or otherwise in electon counts.',
        'standard_fits_keyword': 'ADU',
        'required_keyword': False,
    }),
])
