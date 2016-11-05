"""
``httm.data_structures.metadata``
===================================

This module contains metadata for use in transformation functions.

  - `parameters` is metadata describing various parameters that transformation functions might use.
  - `transformation_flags` is metadata describing status flags so that transformations are not accidentally
    run more than once over the same data.
"""

from collections import OrderedDict

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
        'documentation': 'TODO',
        'default': 11,
    }),
    ('right_dark_pixel_columns', {
        'type': 'int',
        'documentation': 'TODO',
        'default': 11,
    }),
    ('top_dark_pixel_rows', {
        'type': 'int',
        'documentation': 'TODO',
        'default': 10,
    }),
    ('smear_rows', {
        'type': 'int',
        'documentation': 'TODO',
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
        'default': 200000.0,
    }),
    ('blooming_threshold', {
        'type': 'float',
        'documentation': 'The expected maximum number of electrons before a pixel blooms.',
        'default': 150000.0,
    }),
    ('compression', {
        'type': 'float',
        'documentation': 'TODO: This needs a description',
        'default': 0.01,
    }),
    ('undershoot', {
        'type': 'float',
        'documentation': 'TODO: This needs a description',
        'default': 0.001,
    }),
    ('baseline_adu', {
        'type': 'float',
        'documentation': 'TODO: This needs a description',
        'default': 6000.0,
    }),
    ('drift_adu', {
        'type': 'float',
        'documentation': 'TODO: This needs a description',
        'default': 10.0,
    }),
    ('smear_ratio', {
        'type': 'float',
        'documentation': 'TODO: This needs a description. '
                         'Mention how default is derived from ``Hemiola.fpe``',
        'default': 9.79541e-06
    }),
    ('clip_level_adu', {
        'type': 'int',
        'documentation': 'TODO: This needs a description',
        'default': 60000,
    }),
    ('start_of_line_ringing', {
        'type': ':py:class:`numpy.ndarray`',
        'documentation': 'TODO: This needs a description',
        'default': 'TODO',
    }),
    ('pattern_noise', {
        'type': ':py:class:`numpy.ndarray`',
        'documentation': 'TODO: This needs a description',
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
