"""
``httm.fits_utilities.raw_fits``
================================

This module contains functions for marshalling and de-marshalling
:py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter` and the other book-keeping objects
it contains to and from FITS files or :py:class:`astropy.io.fits.HDUList`s.
"""
import astropy
import numpy
from astropy.io.fits import HDUList, PrimaryHDU

from ..data_structures.common import Slice, FITSMetaData
from ..data_structures.raw_converter import SingleCCDRawConverterFlags, SingleCCDRawConverter, \
    raw_transformation_flags, SingleCCDRawConverterParameters, raw_converter_parameters


# noinspection PyUnresolvedReferences
def raw_converter_to_HDUList(converter):
    # type: (SingleCCDRawConverter) -> HDUList
    """
    TODO: Document me

    :param converter:
    :return:
    """
    # noinspection PyTypeChecker
    left_dark_pixel_columns = converter.parameters.left_dark_pixel_columns  # type: int
    right_dark_pixel_columns = converter.parameters.right_dark_pixel_columns  # type: int
    left_dark_parts = [raw_slice.pixels[:, :left_dark_pixel_columns]
                       for raw_slice in converter.slices]  # type: list
    right_dark_parts = [raw_slice.pixels[:, -right_dark_pixel_columns:]
                        for raw_slice in converter.slices]  # type: list
    image_parts = [raw_slice.pixels[:, left_dark_pixel_columns:-right_dark_pixel_columns]
                   for raw_slice in converter.slices]  # type: list

    for i in range(1, len(converter.slices), 2):
        left_dark_parts[i] = numpy.fliplr(left_dark_parts[i])
        right_dark_parts[i] = numpy.fliplr(right_dark_parts[i])
        image_parts[i] = numpy.fliplr(image_parts[i])

    # TODO: Write parameters and flags to HDU header

    # `+` concatenates regular python lists
    return HDUList(PrimaryHDU(header=converter.fits_metadata.header,
                              data=numpy.hstack(left_dark_parts + image_parts + right_dark_parts)))


def write_raw_fits(converter, output_file):
    # type: (SingleCCDRawConverter, str) -> NoneType
    """
    Write a completed :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter`
    to a (simulated) raw FITS file

    :param converter:
    :type converter: :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter`
    :param output_file:
    :type output_file: :py:class:`file` or :py:class:`str`
    :rtype: NoneType
    """
    raw_converter_to_HDUList(converter).writeto(output_file, clobber=True)


def raw_converter_flags_from_fits(input_file,
                                  smear_rows_present=None,
                                  undershoot_present=None,
                                  pattern_noise_present=None,
                                  start_of_line_ringing_present=None,
                                  baseline_present=None,
                                  in_adu=None
                                  ):
    """
    Construct a :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverterFlags`
    from a FITS file, file name or HDUList.

    TODO: Document me

    :param smear_rows_present:
    :type smear_rows_present: bool
    :param undershoot_present:
    :type undershoot_present: bool
    :param pattern_noise_present:
    :type pattern_noise_present: bool
    :param start_of_line_ringing_present:
    :type start_of_line_ringing_present: bool
    :param baseline_present:
    :type baseline_present: bool
    :param in_adu:
    :type in_adu: bool
    :param input_file: The file or file name to input
    :type input_file: :py:class:`file` or :py:class:`str`
    :rtype: :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverterFlags`
    """

    def get_parameter(parameter_name, parameter):
        return raw_transformation_flags[parameter_name]['default'] if parameter is None else parameter

    return SingleCCDRawConverterFlags(
        smear_rows_present=get_parameter('smear_rows_present', smear_rows_present),
        undershoot_present=get_parameter('undershoot_present', undershoot_present),
        pattern_noise_present=get_parameter('pattern_noise_present', pattern_noise_present),
        start_of_line_ringing_present=get_parameter('start_of_line_ringing_present', start_of_line_ringing_present),
        baseline_present=get_parameter('baseline_present', baseline_present),
        in_adu=get_parameter('in_adu', in_adu),
    )


def raw_converter_parameters_from_fits(input_file,
                                       number_of_slices=None,
                                       camera_number=None,
                                       ccd_number=None,
                                       number_of_exposures=None,
                                       video_scales=None,
                                       left_dark_pixel_columns=None,
                                       right_dark_pixel_columns=None,
                                       top_dark_pixel_rows=None,
                                       smear_rows=None,
                                       gain_loss=None,
                                       undershoot_parameter=None,
                                       pattern_noise=None,
                                       ):
    """
    TODO: Document this

    :param input_file:
    :param number_of_slices:
    :param camera_number:
    :param ccd_number:
    :param number_of_exposures:
    :param video_scales:
    :param left_dark_pixel_columns:
    :param right_dark_pixel_columns:
    :param top_dark_pixel_rows:
    :param smear_rows:
    :param gain_loss:
    :param undershoot_parameter:
    :param pattern_noise:
    :return:
    """

    def get_parameter(parameter_name, parameter):
        return raw_converter_parameters[parameter_name]['default'] if parameter is None else parameter

    return SingleCCDRawConverterParameters(
        number_of_slices=get_parameter('number_of_slices', number_of_slices),
        camera_number=get_parameter('camera_number', camera_number),
        ccd_number=get_parameter('ccd_number', ccd_number),
        number_of_exposures=get_parameter('number_of_exposures', number_of_exposures),
        video_scales=get_parameter('video_scales', video_scales),
        left_dark_pixel_columns=get_parameter('left_dark_pixel_columns', left_dark_pixel_columns),
        right_dark_pixel_columns=get_parameter('right_dark_pixel_columns', right_dark_pixel_columns),
        top_dark_pixel_rows=get_parameter('top_dark_pixel_rows', top_dark_pixel_rows),
        smear_rows=get_parameter('smear_rows', smear_rows),
        gain_loss=get_parameter('gain_loss', gain_loss),
        undershoot_parameter=get_parameter('undershoot_parameter', undershoot_parameter),
        pattern_noise=get_parameter('pattern_noise', pattern_noise),
    )


def make_slice_from_raw_data(
        image_and_smear_pixels,
        index,
        left_dark_pixel_columns,
        right_dark_pixel_columns):
    # type: (numpy.ndarray, int, numpy.ndarray, numpy.ndarray) -> Slice
    """
    Construct a slice from raw pixel data given a specified index.

    Result is in *Analogue to Digital Converter Units* (ADU).

    :param image_and_smear_pixels: Image pixels from the calibrated data.
    :type image_and_smear_pixels: :py:class:`numpy.ndarray`
    :param index: The index of the slice to construct.
    :type index: int
    :param left_dark_pixel_columns: The leftmost columns are dark pixels, to be placed on the \
    left of the slice.
    :type left_dark_pixel_columns: :py:class:`numpy.ndarray`
    :param right_dark_pixel_columns: The rightmost columns are dark pixels, to be placed on the \
    right of the slice.
    :type right_dark_pixel_columns: :py:class:`numpy.ndarray`
    :rtype: :py:class:`~httm.data_structures.common.Slice`
    """
    return Slice(
        pixels=numpy.hstack([left_dark_pixel_columns, image_and_smear_pixels, right_dark_pixel_columns]),
        index=index,
        units='ADU')


# TODO write raw_converter_from_HDUList
# noinspection PyUnresolvedReferences
def raw_converter_from_HDUList(header_data_unit_list,
                               origin_file_name=None,
                               flags=None,
                               parameters=None,
                               ):
    """
    TODO: Document this

    :param header_data_unit_list:
    :param origin_file_name:
    :param flags:
    :param parameters:
    :return:
    """
    from numpy import hsplit, fliplr
    flags = raw_converter_flags_from_fits(header_data_unit_list) if flags is None else flags
    parameters = raw_converter_parameters_from_fits(header_data_unit_list) if parameters is None else parameters
    assert len(header_data_unit_list) == 1, "Only a single image per FITS file is supported"
    assert header_data_unit_list[0].data.shape[1] % parameters.number_of_slices == 0, \
        "Image did not have the specified number of slices"

    left_dark_pixel_count = parameters.number_of_slices * parameters.left_dark_pixel_columns
    right_dark_pixel_count = parameters.number_of_slices * parameters.right_dark_pixel_columns
    sliced_image_smear_and_dark_pixels = hsplit(
        header_data_unit_list[0].data[:, left_dark_pixel_count:-right_dark_pixel_count], parameters.number_of_slices)

    # TODO: Document this in layout.rst
    # Rows in odd numbered slices have to be reversed
    for i in range(1, parameters.number_of_slices, 2):
        sliced_image_smear_and_dark_pixels[i] = fliplr(sliced_image_smear_and_dark_pixels[i])

    # Note that left and right dark pixels do not need to be reversed
    sliced_left_dark_pixels = hsplit(header_data_unit_list[0].data[:, :left_dark_pixel_count],
                                     parameters.number_of_slices)
    sliced_right_dark_pixels = hsplit(header_data_unit_list[0].data[:, -right_dark_pixel_count:],
                                      parameters.number_of_slices)

    return SingleCCDRawConverter(
        slices=tuple(map(make_slice_from_raw_data,
                         sliced_image_smear_and_dark_pixels,
                         range(parameters.number_of_slices),
                         sliced_left_dark_pixels,
                         sliced_right_dark_pixels)),
        fits_metadata=FITSMetaData(origin_file_name=origin_file_name,
                                   header=header_data_unit_list[0].header),
        parameters=parameters,
        flags=flags,
    )


def raw_converter_from_fits(input_file, flags=None, parameters=None):
    """
    TODO: Document this

    :param input_file:
    :param flags:
    :param parameters:
    :return:
    """
    header_data_unit_list = astropy.io.fits.open(input_file) if not isinstance(input_file, astropy.io.fits.HDUList) \
        else input_file
    origin_file_name = None
    if isinstance(input_file, str):
        origin_file_name = input_file
    if hasattr(input_file, 'name'):
        origin_file_name = input_file.name
    return raw_converter_from_HDUList(header_data_unit_list,
                                      origin_file_name=origin_file_name,
                                      flags=flags,
                                      parameters=parameters)
