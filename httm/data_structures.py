from collections import namedtuple, OrderedDict

parameters = OrderedDict([
    ('number_of_slices', {
        'type': 'int',
        'documentation': 'The number of slices to use in the transformation, either `1` or `4`',
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
                         'Corresponds to fluctuations in electron counts for completely dark pixel data.',
        'default': (9.5, 9.5, 9.5, 9.5),
    }),
    ('full_well', {
        'type': 'float',
        'documentation': 'The expected maximum number of electrons before a pixel blooms.',
        'default': 200000.0,
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
        'documentation': 'TODO: This needs a description. Mention how default is derived from `Hemiola.fpe`',
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

calibrated_transformation_parameters = parameters
raw_transformation_parameters = OrderedDict((k, parameters[k])
                                            for k in ['number_of_slices',
                                                      'video_scales',
                                                      'compression',
                                                      'undershoot',
                                                      'smear_ratio',
                                                      'clip_level_adu',
                                                      'pattern_noise'])

calibrated_transformation_flags = OrderedDict([
    ('smeared', {
        'type': 'boolean',
        'documentation': 'Indicates whether there is data in the smear rows',
        'default': False,
    }),
    ('readout_noise_added', {
        'type': 'boolean',
        'documentation': 'Indicates whether *readout noise* has been added',
        'default': False,
    }),
    ('shot_noise_added', {
        'type': 'boolean',
        'documentation': 'Indicates whether *shot noise* has been added',
        'default': False,
    }),
    ('blooming_simulated', {
        'type': 'boolean',
        'documentation': 'Indicates whether *blooming* has been simulated',
        'default': False,
    }),
    ('undershoot', {
        'type': 'boolean',
        'documentation': 'Indicates whether *undershoot* is present',
        'default': False,
    }),
    ('pattern_noise', {
        'type': 'boolean',
        'documentation': 'Indicates whether *pattern noise* is present',
        'default': False,
    }),
    ('start_of_line_ringing', {
        'type': 'boolean',
        'documentation': 'Indicates whether *start of line ringing* is present',
        'default': False,
    })
])

raw_transformation_flags = OrderedDict([
    ('smeared', {
        'type': 'boolean',
        'documentation': calibrated_transformation_flags['smeared']['documentation'],
        'default': True,
    }),
    ('undershoot', {
        'type': 'boolean',
        'documentation': calibrated_transformation_flags['undershoot']['documentation'],
        'default': True,
    }),
    ('pattern_noise', {
        'type': 'boolean',
        'documentation': calibrated_transformation_flags['pattern_noise']['documentation'],
        'default': True,
    }),
    ('start_of_line_ringing', {
        'type': 'boolean',
        'documentation': calibrated_transformation_flags['start_of_line_ringing']['documentation'],
        'default': True,
    })
])


def document_parameters(parameter_dictionary):
    """
    Construct a documentation string for dictionary of parameters

    :param parameter_dictionary: An ordered dictionary of parameters,\
    where each entry contains a `type`, documentation string and default value.
    :type parameter_dictionary: :py:class:`collections.OrderedDict`
    :rtype: str
    """
    return '\n'.join([":param {parameter}: {documentation}. Default: `{default}`\n"
                      ":type {parameter}: {type}"
                     .format(parameter=parameter,
                             documentation=data['documentation'].rstrip(". "),
                             default=data['default'],
                             type=data['type'])
                      for parameter, data in parameter_dictionary.iteritems()])


# noinspection PyUnresolvedReferences
class CalibratedConverterParameters(namedtuple('CalibratedConverterParameters',
                                               calibrated_transformation_parameters.keys())):
    __doc__ = """
Converter parameters for converting a calibrated FITS image into an uncalibrated FITS image.

See :py:func:`~httm.calibrated_transform_from_file` for default parameter values.

{parameter_documentation}
""".format(parameter_documentation=document_parameters(calibrated_transformation_parameters))
    __slots__ = ()


# noinspection PyTypeChecker
CalibratedConverterParameters.__new__.__defaults__ = tuple(
    parameter_info['default'] for parameter_info in calibrated_transformation_parameters.values())


# noinspection PyUnresolvedReferences
class RAWConverterParameters(
    namedtuple('RAWConverterParameters',
               raw_transformation_parameters.keys())):
    __doc__ = """
Converter parameters for converting a calibrated FITS image into an uncalibrated FITS image.

{parameter_documentation}
""".format(parameter_documentation=document_parameters(raw_transformation_parameters))
    __slots__ = ()


RAWConverterParameters.__new__.__defaults__ = tuple(
    parameter_info['default'] for parameter_info in raw_transformation_parameters.values())


# noinspection PyClassHasNoInit
class CalibratedConverterFlags(
    namedtuple('CalibratedConverterFlags',
               calibrated_transformation_flags.keys())):
    __doc__ = """
Flags indicating which raw transformations have been performed.

{parameter_documentation}
""".format(parameter_documentation=document_parameters(calibrated_transformation_flags))
    __slots__ = ()


CalibratedConverterFlags.__new__.__defaults__ = tuple(
    parameter_info['default'] for parameter_info in calibrated_transformation_flags.values())


# noinspection PyClassHasNoInit
class RawConverterFlags(
    namedtuple('RawConverterFlags',
               raw_transformation_flags.keys())):
    __doc__ = """
Flags indicating which raw transformations have been performed.

{parameter_documentation}
""".format(parameter_documentation=document_parameters(raw_transformation_flags))
    __slots__ = ()


RawConverterFlags.__new__.__defaults__ = tuple(
    parameter_info['default'] for parameter_info in raw_transformation_flags.values())


# noinspection PyUnresolvedReferences,PyClassHasNoInit
class FITSMetaData(
    namedtuple('FITSMetaData',
               ['origin_file_name', 'header'])):
    """
    Meta data associated with data taken from a FITS file.

    :param origin_file_name: The original file name where the data was taken from
    :type origin_file_name: str
    :param header: The header of the FITS file where the data was taken from
    :type header: :py:class:`pyfits.Header`
    """
    __slots__ = ()


# noinspection PyUnresolvedReferences,PyClassHasNoInit
class Slice(
    namedtuple('Slice',
               ['index',
                'units',
                'pixels'])):
    """
    A slice from a CCD. Includes all data associated with the slice in question
    from various parts of the raw CCD image.


    :param index: The index of the slice in the CCD
    :param units: Can be either `electrons` or `ADU`
    :type units: str
    :param pixels: The slice image data
    :type pixels: :py:class:`numpy.ndarray`
    """
    __slots__ = ()


# noinspection PyProtectedMember
Slice.__new__.__defaults__ = (None,) * len(Slice._fields)


# noinspection PyUnresolvedReferences,PyClassHasNoInit
class CalibratedConverter(
    namedtuple('CalibratedConverter',
               ['slices',
                'fits_metadata',
                'parameters',
                'flags'])):
    """
    An immutable object for managing a transformation from a calibrated FITS image into a (simulated) raw image.

    :param slices: The slices of the image
    :type slices: tuple of :py:class:`~httm.data_structures.Slice` objects
    :param fits_metadata: Meta data associated with the image
    :type fits_metadata: :py:class:`~httm.data_structures.FITSMetaData`
    :param parameters: The parameters of the transformation
    :type parameters: :py:class:`~httm.data_structures.CalibratedConverterParameters`
    :param flags: Flags indicating the state of the transformation
    :type flags: :py:class:`~httm.data_structures.CalibratedConverterFlags`
    """


# noinspection PyUnresolvedReferences,PyClassHasNoInit
class RAWConverter(
    namedtuple('RAWConverter',
               ['slices',
                'fits_metadata',
                'parameters',
                'flags'])):
    """
    An immutable object for managing a transformation from a raw FITS image into a calibrated image.

    :param slices: The slices of the image
    :type slices: list of :py:class:`~httm.data_structures.Slice` objects
    :param fits_metadata: Meta data associated with the image
    :type fits_metadata: :py:class:`~httm.data_structures.FITSMetaData`
    :param parameters: The parameters of the transformation
    :type parameters: :py:class:`~httm.data_structures.RAWConverterParameters`
    :param flags: Flags indicating the state of the transformation
    :type flags: :py:class:`~httm.data_structures.RawConverterFlags`
    """
    __slots__ = ()
