"""
``httm.fits_utilities.calibrated_fits``
=======================================

This module contains functions for marshalling and de-marshalling
:py:class:`~httm.data_structures.calibrated_converter.SingleCCDCalibratedConverter` and the other book-keeping objects
it contains from a FITS file or :py:class:`astropy.io.fits.HDUList`.
"""
import astropy
import numpy
from astropy.io.fits import HDUList, PrimaryHDU

from ..data_structures.calibrated_converter import SingleCCDCalibratedConverterFlags, calibrated_transformation_flags, \
    SingleCCDCalibratedConverterParameters, SingleCCDCalibratedConverter, calibrated_converter_parameters
from ..data_structures.common import Slice, FITSMetaData


def make_slice_from_calibrated_data(pixels,
                                    left_dark_pixel_columns,
                                    right_dark_pixel_columns,
                                    top_dark_pixel_rows,
                                    smear_rows,
                                    index):
    # type: (numpy.ndarray, int, int, int, int, int) -> Slice
    """
    Construct a slice from an array of calibrated pixel data given a specified index.

    Result is in *electron* counts.

    :param pixels: Image pixels from the calibrated data.
    :type pixels: :py:class:`numpy.ndarray`
    :param left_dark_pixel_columns:
    :type left_dark_pixel_columns: int
    :param right_dark_pixel_columns:
    :type right_dark_pixel_columns: int
    :param top_dark_pixel_rows:
    :type top_dark_pixel_rows: int
    :param smear_rows:
    :type smear_rows: int
    :param index: The index of the slice to construct.
    :type index: int
    :rtype: :py:class:`~httm.data_structures.common.Slice`
    """
    image_and_smear_and_top_dark_pixels = numpy.vstack(
        [pixels, numpy.zeros((top_dark_pixel_rows + smear_rows, pixels.shape[1]))])
    row_count = image_and_smear_and_top_dark_pixels.shape[0]
    left_dark_pixels = numpy.zeros((row_count, left_dark_pixel_columns))
    right_dark_pixels = numpy.zeros((row_count, right_dark_pixel_columns))
    return Slice(pixels=numpy.hstack([left_dark_pixels, image_and_smear_and_top_dark_pixels, right_dark_pixels]),
                 index=index,
                 units='electrons')


def calibrated_converter_flags_from_fits(input_file,
                                         smear_rows_present=None,
                                         readout_noise_present=None,
                                         shot_noise_present=None,
                                         blooming_present=None,
                                         undershoot_present=None,
                                         pattern_noise_present=None,
                                         start_of_line_ringing_present=None,
                                         baseline_present=None,
                                         in_adu=None,
                                         ):
    """
    Construct a :py:class:`~httm.data_structures.calibrated_converter.SingleCCDCalibratedConverterFlags`
    from a file or file name.

    :param input_file: The file or file name to input
    :type input_file: :py:class:`file` or :py:class:`str`
    :param smear_rows_present: Flag that indicates if *smear rows* are already present or have otherwise been \
    removed
    :type smear_rows_present: bool
    :param readout_noise_present: Flag that indicates if *readout noise* has been simulated or has otherwise been \
    removed
    :type readout_noise_present: bool
    :param shot_noise_present: Flag that indicates *shot noise* has not been simulated
    :type shot_noise_present: bool
    :param blooming_present: Flag that indicates *blooming* has been simulated
    :type blooming_present: bool
    :param undershoot_present: Flag indicates that *undershoot* has been simulated or has otherwise been removed
    :type undershoot_present: bool
    :param pattern_noise_present: Flag indicates that *pattern noise* has been simulated or has otherwise been removed
    :type pattern_noise_present: bool
    :param start_of_line_ringing_present: Flag that indicates *start of line ringing* has been simulated
    :type start_of_line_ringing_present: bool
    :param in_adu:
    :type in_adu: bool
    :rtype: :py:class:`~httm.data_structures.calibrated_converter.SingleCCDCalibratedConverterFlags`
    """

    def get_parameter(parameter_name, parameter):
        return calibrated_transformation_flags[parameter_name]['default'] if parameter is None else parameter

    # TODO try to read these from file
    return SingleCCDCalibratedConverterFlags(
        smear_rows_present=get_parameter('smear_rows_present', smear_rows_present),
        readout_noise_present=get_parameter('readout_noise_present', readout_noise_present),
        shot_noise_present=get_parameter('shot_noise_present', shot_noise_present),
        blooming_present=get_parameter('blooming_present', blooming_present),
        undershoot_present=get_parameter('undershoot_present', undershoot_present),
        pattern_noise_present=get_parameter('pattern_noise_present', pattern_noise_present),
        start_of_line_ringing_present=get_parameter('start_of_line_ringing_present',
                                                    start_of_line_ringing_present),
        baseline_present=get_parameter('baseline_present', baseline_present),
        in_adu=get_parameter('in_adu', in_adu),
    )


def calibrated_converter_parameters_from_fits(input_file,
                                              number_of_slices=None,
                                              camera_number=None,
                                              ccd_number=None,
                                              number_of_exposures=None,
                                              video_scales=None,
                                              readout_noise_parameters=None,
                                              left_dark_pixel_columns=None,
                                              right_dark_pixel_columns=None,
                                              top_dark_pixel_rows=None,
                                              smear_rows=None,
                                              random_seed=None,
                                              full_well=None,
                                              gain_loss=None,
                                              undershoot_parameter=None,
                                              single_frame_baseline_adus=None,
                                              single_frame_baseline_adu_drift_term=None,
                                              smear_ratio=None,
                                              clip_level_adu=None,
                                              start_of_line_ringing=None,
                                              pattern_noise=None,
                                              blooming_threshold=None,
                                              ):
    """
    TODO: Document me

    :param input_file:
    :param number_of_slices:
    :param camera_number:
    :param ccd_number:
    :param number_of_exposures:
    :param video_scales:
    :param readout_noise_parameters:
    :param left_dark_pixel_columns:
    :param right_dark_pixel_columns:
    :param top_dark_pixel_rows:
    :param smear_rows:
    :param random_seed:
    :param full_well:
    :param gain_loss:
    :param undershoot_parameter:
    :param single_frame_baseline_adus:
    :param single_frame_baseline_adu_drift_term:
    :param smear_ratio:
    :param clip_level_adu:
    :param start_of_line_ringing:
    :param pattern_noise:
    :param blooming_threshold:
    :return:
    """

    def get_parameter(parameter_name, parameter):
        return calibrated_converter_parameters[parameter_name]['default'] if parameter is None else parameter

    return SingleCCDCalibratedConverterParameters(
        number_of_slices=get_parameter('number_of_slices', number_of_slices),
        camera_number=get_parameter('camera_number', camera_number),
        ccd_number=get_parameter('ccd_number', ccd_number),
        number_of_exposures=get_parameter('number_of_exposures', number_of_exposures),
        video_scales=get_parameter('video_scales', video_scales),
        readout_noise_parameters=get_parameter('readout_noise_parameters', readout_noise_parameters),
        left_dark_pixel_columns=get_parameter('left_dark_pixel_columns', left_dark_pixel_columns),
        right_dark_pixel_columns=get_parameter('right_dark_pixel_columns', right_dark_pixel_columns),
        top_dark_pixel_rows=get_parameter('top_dark_pixel_rows', top_dark_pixel_rows),
        smear_rows=get_parameter('smear_rows', smear_rows),
        random_seed=get_parameter('random_seed', random_seed),
        full_well=get_parameter('full_well', full_well),
        gain_loss=get_parameter('gain_loss', gain_loss),
        undershoot_parameter=get_parameter('undershoot_parameter', undershoot_parameter),
        single_frame_baseline_adus=get_parameter('single_frame_baseline_adus', single_frame_baseline_adus),
        single_frame_baseline_adu_drift_term=get_parameter('single_frame_baseline_adu_drift_term',
                                                           single_frame_baseline_adu_drift_term),
        smear_ratio=get_parameter('smear_ratio', smear_ratio),
        clip_level_adu=get_parameter('clip_level_adu', clip_level_adu),
        start_of_line_ringing=get_parameter('start_of_line_ringing', start_of_line_ringing),
        pattern_noise=get_parameter('pattern_noise', pattern_noise),
        blooming_threshold=get_parameter('blooming_threshold', blooming_threshold),
    )


def calibrated_converter_to_HDUList(converter):
    # type: (SingleCCDCalibratedConverter) -> HDUList
    """
    This function converts a :py:class:`~httm.data_structures.calibrated_converter.SingleCCDCalibratedConverter`
    into an :py:class:`astropy.io.fits.HDUList` object, suitable for writing out to a (simulated) raw FITS file.

    :param converter: A calibrated converter object
    :type converter: :py:class:`~httm.data_structures.calibrated_converter.SingleCCDCalibratedConverter`
    :rtype: :py:class:`astropy.io.fits.HDUList`
    """
    # TODO: write parameters and flags to HDU Headers
    left_dark_pixel_columns = converter.parameters.left_dark_pixel_columns
    right_dark_pixel_columns = converter.parameters.right_dark_pixel_columns
    top_dark_pixel_rows = converter.parameters.top_dark_pixel_rows
    smear_rows = converter.parameters.smear_rows
    slices = [raw_slice.pixels[:-(top_dark_pixel_rows + smear_rows), left_dark_pixel_columns:-right_dark_pixel_columns]
              for raw_slice in converter.slices]
    for i in range(1, len(slices), 2):
        slices[i] = numpy.fliplr(slices[i])
    return HDUList(PrimaryHDU(header=converter.fits_metadata.header,
                              data=numpy.hstack(slices)))


def write_calibrated_fits(converter, output_file):
    # type: (SingleCCDCalibratedConverter, str) -> NoneType
    """
    Write a :py:class:`~httm.data_structures.calibrated_converter.SingleCCDCalibratedConverter`
    to a (simulated) raw FITS file.

    :param converter:
    :type converter: :py:class:`~httm.data_structures.calibrated_converter.SingleCCDCalibratedConverter`
    :param output_file:
    :type output_file: str
    :rtype: NoneType
    """
    calibrated_converter_to_HDUList(converter).writeto(output_file)


# noinspection PyUnresolvedReferences
def calibrated_converter_from_HDUList(header_data_unit_list, origin_file_name=None, flags=None, parameters=None):
    """
    TODO: Document me

    :param header_data_unit_list:
    :param origin_file_name:
    :param flags:
    :param parameters:
    :return:
    """
    flags = calibrated_converter_flags_from_fits(header_data_unit_list) if flags is None else flags
    parameters = calibrated_converter_parameters_from_fits(
        header_data_unit_list) if parameters is None else parameters  # type: SingleCCDCalibratedConverterParameters
    assert len(header_data_unit_list) == 1, "Only a single image per FITS file is supported"
    assert header_data_unit_list[0].data.shape[1] % parameters.number_of_slices == 0, \
        "Image did not have the specified number of slices"
    return SingleCCDCalibratedConverter(
        slices=map(lambda pixel_data, index:
                   make_slice_from_calibrated_data(pixel_data,
                                                   parameters.left_dark_pixel_columns,
                                                   parameters.right_dark_pixel_columns,
                                                   parameters.top_dark_pixel_rows,
                                                   parameters.smear_rows,
                                                   index),
                   numpy.hsplit(header_data_unit_list[0].data, parameters.number_of_slices),
                   range(parameters.number_of_slices)),
        fits_metadata=FITSMetaData(origin_file_name=origin_file_name,
                                   header=header_data_unit_list[0].header),
        parameters=parameters,
        flags=flags,
    )


def calibrated_converter_from_fits(input_file, flags=None, parameters=None):
    """
    TODO: Document me

    :param input_file:
    :param flags:
    :param parameters:
    :return:
    """
    header_data_unit_list = astropy.io.fits.open(input_file) if not isinstance(input_file,
                                                                               astropy.io.fits.HDUList) else input_file
    origin_file_name = None
    if isinstance(input_file, str):
        origin_file_name = input_file
    if hasattr(input_file, 'name'):
        origin_file_name = input_file.name
    return calibrated_converter_from_HDUList(header_data_unit_list,
                                             origin_file_name=origin_file_name,
                                             flags=flags,
                                             parameters=parameters)
