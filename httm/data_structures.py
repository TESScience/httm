import numpy
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
                         '*Analogue to Digital Converter Units* (ADU) to electron counts.'
                         'These have units of electrons per ADU.',
        'default': (5.5, 5.5, 5.5, 5.5),
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

calibrated_transform_parameters = parameters
raw_transform_parameters = OrderedDict((k, parameters[k])
                                       for k in ['number_of_slices',
                                                 'video_scales',
                                                 'compression',
                                                 'undershoot',
                                                 'smear_ratio',
                                                 'clip_level_adu',
                                                 'pattern_noise'])


def document_parameters(parameter_dictionary):
    """
    Construct a documentation string for dictionary of parameters

    :param parameter_dictionary: An ordered dictionary of parameters,\
    where each entry contains a `type`, documentation string and default value.
    :type parameter_dictionary: :py:class:`collections.OrderedDict`
    :rtype: str
    """
    return '\n'.join([":param {parameter}: {documentation}\n"
                      ":type {parameter}: {type}".format(parameter=parameter,
                                                         documentation=data['documentation'],
                                                         type=data['type'])
                      for parameter, data in parameter_dictionary.iteritems()])


default_calibrated_transform_parameters = {
    'video_scales': (5.5, 5.5, 5.5, 5.5),  # electrons/ADU
    'number_of_slices': 4,  # number of slices to use in transformation, either 1 or 4
    'compression': 0.01,
    'undershoot': 0.001,
    'baseline_adu': 6000.0,
    'drift_adu': 10.0,
    'smear_ratio': 9.79541e-6,  # Derived from Hemiola.fpe
    'clip_level_adu': 60000,
    'start_of_line_ringing': numpy.zeros(534),  # TODO: Read this from a file
    'pattern_noise': numpy.zeros((2078, 534))  # TODO: Read this from a file
}

default_raw_transform_parameters = {
    k: default_calibrated_transform_parameters[k]
    for k in [
        'video_scales',
        'number_of_slices',
        'compression',
        'undershoot',
        'smear_ratio',
        'clip_level_adu',
        'pattern_noise'
    ]}


# noinspection PyUnresolvedReferences
class CalibratedTransformParameters(namedtuple('CalibratedTransformParameters',
                                               calibrated_transform_parameters.keys())):
    __doc__ = """
Transformation parameters for converting a calibrated FITS image into an uncalibrated FITS image.

See :py:func:`~httm.calibrated_transform_from_file` for default parameter values.

{parameter_documentation}
""".format(parameter_documentation=document_parameters(calibrated_transform_parameters))
    __slots__ = ()


# noinspection PyTypeChecker
CalibratedTransformParameters.__new__.__defaults__ = tuple(
    parameter_info['default'] for parameter_info in calibrated_transform_parameters.values())


# noinspection PyUnresolvedReferences
class RAWTransformParameters(
    namedtuple('RAWTransformParameters',
               default_raw_transform_parameters.keys())):
    __doc__ = """
Transformation parameters for converting a calibrated FITS image into an uncalibrated FITS image.

{parameter_documentation}
""".format(parameter_documentation=document_parameters(raw_transform_parameters))
    __slots__ = ()


RAWTransformParameters.__new__.__defaults__ = tuple(default_raw_transform_parameters.values())


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

    :param smear_rows:
    :param top_dark_pixel_rows:
    :param left_dark_pixel_columns:
    :param right_dark_pixel_columns:
    :param index: The index of the slice in the CCD
    :param units: Can be either `electrons` or `ADU`
    :type units: str
    :param pixels: The image data in the pixel
    """
    __slots__ = ()


# noinspection PyProtectedMember
Slice.__new__.__defaults__ = (None,) * len(Slice._fields)


# noinspection PyUnresolvedReferences,PyClassHasNoInit
class RAWTransformation(
    namedtuple('RAWTransformation',
               ['slices',
                'fits_metadata',
                'parameters'])):
    """
    An immutable object for managing a transformation from a raw FITS image into a calibrated image.

    :param slices: The slices of the image
    :type slices: list of :py:class:`~httm.data_structures.Slice` objects
    :param fits_metadata: Meta data associated with the image
    :type fits_metadata: :py:class:`~httm.data_structures.FITSMetaData`
    :param parameters: The parameters of the transformation
    :type parameters: :py:class:`~httm.data_structures.RAWTransformParameters`
    """
    __slots__ = ()


# noinspection PyUnresolvedReferences,PyClassHasNoInit
class CalibratedTransformation(
    namedtuple('CalibratedTransformation',
               ['slices',
                'fits_metadata',
                'parameters'])):
    """
    An immutable object for managing a transformation from a calibrated FITS image into a (simulated) raw image.

    :param slices: The slices of the image
    :type slices: tuple of :py:class:`~httm.data_structures.Slice` objects
    :param fits_metadata: Meta data associated with the image
    :type fits_metadata: :py:class:`~httm.data_structures.FITSMetaData`
    :param parameters: The parameters of the transformation
    :type parameters: :py:class:`~httm.data_structures.CalibratedTransformParameters`
    """
