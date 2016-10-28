import numpy
from collections import namedtuple

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
class CalibratedTransformParameters(
    namedtuple('CalibratedTransformParameters',
               default_calibrated_transform_parameters.keys())):
    """
    Transformation parameters for converting a calibrated FITS image into an uncalibrated FITS image.

    :param video_scales: The video scaling constants, for converting back and forth between\
     *Analogue to Digital Converter Units* (ADU) to electron counts.\
      These have units of electrons per ADU.
    :type video_scales: tuple of :py:class:`float` objects, must have one for each slice
    :param number_of_slices: The number of slices to make in the resulting uncalibrated image.
    :type number_of_slices: int
    :param compression: The compression factor.
    :type compression: float
    :param undershoot: The undershoot factor.
    :type undershoot: float
    :param baseline_adu: The baseline adu factor.
    :type baseline_adu: float
    :param drift_adu: The drift ADU factor.
    :type drift_adu: float
    :param smear_ratio: The smear ratio.
    :type smear_ratio: float
    :param clip_level_adu: The clip level ADU.
    :type clip_level_adu: int
    :param start_of_line_ringing: The start of line ringing vector. Default: Read from **TODO**
    :type start_of_line_ringing: :py:class:`numpy.ndarray`
    :param pattern_noise: The pattern noise. Default: Read from **TODO**
    :type pattern_noise: :py:class:`numpy.ndarray`
    """
    __slots__ = ()


CalibratedTransformParameters.__new__.__defaults__ = tuple(default_calibrated_transform_parameters.values())


# noinspection PyUnresolvedReferences
class RAWTransformParameters(
    namedtuple('RAWTransformParameters',
               default_raw_transform_parameters.keys())):
    """
    Transformation parameters for converting a calibrated FITS image into an uncalibrated FITS image.

    :param video_scales:
    :param number_of_slices:
    :param compression:
    :param undershoot:
    :param smear_ratio:
    :param clip_level_adu:
    :param pattern_noise:
    """
    __slots__ = ()


RAWTransformParameters.__new__.__defaults__ = tuple(default_raw_transform_parameters.values())


# noinspection PyUnresolvedReferences
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


# noinspection PyUnresolvedReferences
class Slice(
    namedtuple('Slice',
               ['smear_rows',
                'top_dark_pixel_rows',
                'left_dark_pixel_columns',
                'right_dark_pixel_columns',
                'index',
                'units',
                'image_pixels'])):
    __doc__ = """
    A slice from a CCD. Includes all data associated with the slice in question
    from various parts of the raw CCD image.

    :param smear_rows:
    :param top_dark_pixel_rows:
    :param left_dark_pixel_columns:
    :param right_dark_pixel_columns:
    :param index: The index of the slice in the CCD
    :param units: Can be either `electrons` or `ADU`
    :type units: str
    :param image_pixels: The image data in the pixel
    """
    __slots__ = ()


Slice.__new__.__defaults__ = (None,) * len(Slice._fields)


# noinspection PyUnresolvedReferences
class RAWTransformation(
    namedtuple('RAWTransformation',
               ['slices',
                'fits_metadata',
                'parameters'])):
    """
    An immutable object for managing a transformation from a raw FITS image into a calibrated image.

    :param slices: The slices of the image
    :type slices: list of :py:class:`~httm.Slice` objects
    :param fits_metadata: Meta data associated with the image
    :type fits_metadata: :py:class:`~httm.FITSMetaData`
    :param parameters: The parameters of the transformation
    :type parameters: :py:class:`~httm.RAWTransformParameters`
    """
    __slots__ = ()


# noinspection PyUnresolvedReferences
class CalibratedTransformation(
    namedtuple('CalibratedTransformation',
               ['slices',
                'fits_metadata',
                'parameters'])):
    """
    An immutable object for managing a transformation from a calibrated FITS image into a (simulated) raw image.

    :param slices: The slices of the image
    :type slices: tuple of :py:class:`~httm.Slice` objects
    :param fits_metadata: Meta data associated with the image
    :type fits_metadata: :py:class:`~httm.FITSMetaData`
    :param parameters: The parameters of the transformation
    :type parameters: :py:class:`~httm.CalibratedTransformParameters`
    """