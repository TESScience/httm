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
    }),
    ('video_scales', {
        'type': 'tuple of :py:class:`float` objects, must have one for each slice',
        'documentation': 'The video scaling constants, for converting back and forth between '
                         '*Analogue to Digital Converter Units* (ADU) to electron counts. '
                         'These have units of electrons per ADU.',
        'default': (5.5, 5.5, 5.5, 5.5),
    }),
    ('readout_noise', {
        'type': 'tuple of :py:class:`float` objects, must have one for each slice',
        'documentation': 'The video readout noise standard deviation in electrons. '
                         'Corresponds to fluctuations in electron counts for completely '
                         'dark pixel data.',
        'default': (9.5, 9.5, 9.5, 9.5),
    }),
    ('left_dark_pixel_columns', {
        'type': 'int',
        'documentation': 'Count of columns of pixels that have never traversed the image area '
	                 'or frame store, and thus were never exposed to light. '
			 'Read before the image pixels in the row, these '
			 'are where most of the start of line ringing may be seen. ',
        'default': 11,
    }),
    ('right_dark_pixel_columns', {
        'type': 'int',
        'documentation': 'Count of columns of pixels that have never traversed the image area '
	                 'or frame store, and thus were never exposed to light. '
			 'Read after the image pixels in a row. ',
        'default': 11,
    }),
    ('top_dark_pixel_rows', {
        'type': 'int',
        'documentation': 'Count of rows of pixels that have traversed the frame store area, '
	                 'but not the image area, and thus were never exposed to light. ',
        'default': 10,
    }),
    ('smear_rows', {
        'type': 'int',
        'documentation': 'Count of rows of pixels that have traversed the imaging area during '
	                 'frame transfer, but have zero exposure to light otherwise. '
			 'These are for estimating the effect of smear on the imaging pixels.',
        'default': 10,
    }),
    ('random_seed', {
        'type': 'int',
        'documentation': 'The seed value to hand to the random number generator',
        'default': None
    }),
    ('full_well', {
        'type': 'float',
        'documentation': 'The expected maximum number of electrons that a pixel can hold.',
        'default': 170000.0,
    }),
    ('blooming_threshold', {
        'type': 'float',
        'documentation': 'The expected maximum number of electrons before a pixel blooms.',
        'default': 140000.0,
    }),
    ('compression', {
        'type': 'float',
        'documentation': 'The relative decrease in video gain over the total ADC range. '
	                 'This is the parameter of our nonlinearity model.',
        'default': 0.01,
    }),
    ('undershoot', {
        'type': 'float',
        'documentation': 'The deficit in a pixel value relative to the value of its '
	                 'preceeding pixel. The electronics have a slight memory of the '
			 'signal level which cause the pixel following a bright pixel '
			 'to appear slightly darker that it should.',
        'default': 0.0013,
    }),
    ('baseline_adu', {
        'type': 'float',
        'documentation': 'The mean ADC level for a pixel with zero electrons.',
        'default': 6000.0,
    }),
    ('drift_adu', {
        'type': 'float',
        'documentation': 'Standard deviation of a random number added to the baseline_adu '
	                 'per simulated frame, to stress the baseline determination code.',
        'default': 10.0,
    }),
    ('smear_ratio', {
        'type': 'float',
        'documentation': 'The time that a charge packet spends in transit through '
	                 "each imaging pixel that it doesn't nominally belong to, relative "
			 'to the time it spends in the pixel it does nominally belong to. '
			 'Derived from the sequencer program. '
                         'The default is derived from ``Hemiola.fpe``.',
        'default': 4.84836e-06
    }),
    ('clip_level_adu', {
        'type': 'int',
        'documentation': 'The level in ADU where the CCD or the electronics will '
	                 'clip the video. The default is the maximum the ADC can deliver.',
        'default': FPE_MAX_ADU,
    }),
    ('start_of_line_ringing', {
        'type': ':py:class:`numpy.ndarray`',
        'documentation': 'A vector added to each row in the slice, representing the repeatable '
	                 'change in the video baseline caused by the disturbance in the data '
			 'acquisition rhythm between rows. Units are electrons.',
        'default': 'TODO',
    }),
    ('pattern_noise', {
        'type': ':py:class:`numpy.ndarray`',
        'documentation': 'A matrix added to data array for the slice, representing the repeatable '
	                 'change in the video baseline caused by the disturbance in the data '
			 'acquisition rhythm between frames. Units are electrons.',
        'default': 'TODO',
    })
])

transformation_flags = OrderedDict([
    ('smear_rows_present', {
        'type': 'boolean',
        'documentation': 'Indicates whether there is data in the smear rows.',
    }),
    ('readout_noise_added', {
        'type': 'boolean',
        'documentation': 'Indicates whether *readout noise* has been added.',
    }),
    ('shot_noise_added', {
        'type': 'boolean',
        'documentation': 'Indicates whether *shot noise* has been added.',
    }),
    ('blooming_simulated', {
        'type': 'boolean',
        'documentation': 'Indicates whether *blooming* has been simulated.',
    }),
    ('undershoot_uncompensated', {
        'type': 'boolean',
        'documentation': 'Indicates whether *undershoot* is present or otherwise compensated for.',
    }),
    ('pattern_noise_uncompensated', {
        'type': 'boolean',
        'documentation': 'Indicates whether *pattern noise* is present or otherwise compensated for.',
    }),
    ('start_of_line_ringing_uncompensated', {
        'type': 'boolean',
        'documentation': 'Indicates whether *start of line ringing* is present or otherwise compensated for.',
    })
])
