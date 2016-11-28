"""
``httm.fits_utilities.electron_flux_fits``
==========================================

This module contains functions for marshalling and de-marshalling
:py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`
and the other book-keeping objects it contains to and from FITS files or :py:class:`astropy.io.fits.HDUList` objects.
"""
import astropy
import numpy
from astropy.io.fits import HDUList, PrimaryHDU

from ..data_structures.common import Slice, FITSMetaData
from ..data_structures.electron_flux_converter import SingleCCDElectronFluxConverterFlags, \
    electron_flux_transformation_flags, \
    SingleCCDElectronFluxConverterParameters, SingleCCDElectronFluxConverter, electron_flux_converter_parameters


def make_slice_from_electron_flux_data(pixels,
                                       early_dark_pixel_columns,
                                       late_dark_pixel_columns,
                                       final_dark_pixel_rows,
                                       smear_rows,
                                       index):
    # type: (numpy.ndarray, int, int, int, int, int) -> Slice
    """
    Construct a slice from an array of electron flux pixel data given a specified index.

    Result is in *electron* counts.

    :param pixels: Image pixels from the electron flux data.
    :type pixels: :py:class:`numpy.ndarray`
    :param early_dark_pixel_columns:
    :type early_dark_pixel_columns: int
    :param late_dark_pixel_columns:
    :type late_dark_pixel_columns: int
    :param final_dark_pixel_rows:
    :type final_dark_pixel_rows: int
    :param smear_rows:
    :type smear_rows: int
    :param index: The index of the slice to construct.
    :type index: int
    :rtype: :py:class:`~httm.data_structures.common.Slice`
    """
    image_and_smear_and_final_dark_pixels = numpy.vstack(
        [pixels, numpy.zeros((final_dark_pixel_rows + smear_rows, pixels.shape[1]))])
    row_count = image_and_smear_and_final_dark_pixels.shape[0]
    early_dark_pixels = numpy.zeros((row_count, early_dark_pixel_columns))
    late_dark_pixels = numpy.zeros((row_count, late_dark_pixel_columns))
    return Slice(pixels=numpy.hstack([early_dark_pixels, image_and_smear_and_final_dark_pixels, late_dark_pixels]),
                 index=index,
                 units='electrons')


def electron_flux_converter_flags_from_fits(input_file,
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
    Construct a :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverterFlags`
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
    :param in_adu: Flag that indicates whether the units are in *Analogue to Digital Converter* units or not
    :type in_adu: bool
    :rtype: :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverterFlags`
    """

    def get_parameter(parameter_name, parameter):
        return electron_flux_transformation_flags[parameter_name]['default'] if parameter is None else parameter

    # TODO try to read these from file
    return SingleCCDElectronFluxConverterFlags(
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


def electron_flux_converter_parameters_from_fits(input_file,
                                                 number_of_slices=None,
                                                 camera_number=None,
                                                 ccd_number=None,
                                                 number_of_exposures=None,
                                                 video_scales=None,
                                                 readout_noise_parameters=None,
                                                 early_dark_pixel_columns=None,
                                                 late_dark_pixel_columns=None,
                                                 final_dark_pixel_rows=None,
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
    :param early_dark_pixel_columns:
    :param late_dark_pixel_columns:
    :param final_dark_pixel_rows:
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
        return electron_flux_converter_parameters[parameter_name]['default'] if parameter is None else parameter

    return SingleCCDElectronFluxConverterParameters(
        number_of_slices=get_parameter('number_of_slices', number_of_slices),
        camera_number=get_parameter('camera_number', camera_number),
        ccd_number=get_parameter('ccd_number', ccd_number),
        number_of_exposures=get_parameter('number_of_exposures', number_of_exposures),
        video_scales=get_parameter('video_scales', video_scales),
        readout_noise_parameters=get_parameter('readout_noise_parameters', readout_noise_parameters),
        early_dark_pixel_columns=get_parameter('early_dark_pixel_columns', early_dark_pixel_columns),
        late_dark_pixel_columns=get_parameter('late_dark_pixel_columns', late_dark_pixel_columns),
        final_dark_pixel_rows=get_parameter('final_dark_pixel_rows', final_dark_pixel_rows),
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


def electron_flux_converter_to_simulated_raw_hdulist(converter):
    # type: (SingleCCDElectronFluxConverter) -> HDUList
    """
    This function converts a :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`
    into an :py:class:`astropy.io.fits.HDUList` object, suitable for writing out to a simulated raw FITS file.

    :param converter: An electron flux converter object
    :type converter: :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`
    :rtype: :py:class:`astropy.io.fits.HDUList`
    """
    # TODO: write parameters and flags to HDU Headers
    early_dark_pixel_columns = converter.parameters.early_dark_pixel_columns
    late_dark_pixel_columns = converter.parameters.late_dark_pixel_columns
    final_dark_pixel_rows = converter.parameters.final_dark_pixel_rows
    smear_rows = converter.parameters.smear_rows
    slices = [
        raw_slice.pixels[:-(final_dark_pixel_rows + smear_rows), early_dark_pixel_columns:-late_dark_pixel_columns]
        for raw_slice in converter.slices]
    for i in range(1, len(slices), 2):
        slices[i] = numpy.fliplr(slices[i])
    return HDUList(PrimaryHDU(header=converter.fits_metadata.header,
                              data=numpy.hstack(slices)))


def write_electron_flux_converter_to_simulated_raw_fits(converter, output_file):
    # type: (SingleCCDElectronFluxConverter, str) -> NoneType
    """
    Write a :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`
    to a simulated raw FITS file.

    :param converter:
    :type converter: :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`
    :param output_file:
    :type output_file: str
    :rtype: NoneType
    """
    electron_flux_converter_to_simulated_raw_hdulist(converter).writeto(output_file, clobber=True)


# noinspection PyUnresolvedReferences
def electron_flux_converter_from_hdulist(header_data_unit_list, origin_file_name=None, flags=None, parameters=None):
    """
    TODO: Document me

    :param header_data_unit_list:
    :param origin_file_name:
    :param flags:
    :param parameters:
    :return:
    """
    flags = electron_flux_converter_flags_from_fits(header_data_unit_list) if flags is None else flags
    parameters = electron_flux_converter_parameters_from_fits(
        header_data_unit_list) if parameters is None else parameters  # type: SingleCCDElectronFluxConverterParameters
    assert len(header_data_unit_list) == 1, "Only a single image per FITS file is supported"
    assert header_data_unit_list[0].data.shape[1] % parameters.number_of_slices == 0, \
        "Image did not have the specified number of slices"
    return SingleCCDElectronFluxConverter(
        slices=tuple(map(lambda pixel_data, index:
                         make_slice_from_electron_flux_data(pixel_data,
                                                            parameters.early_dark_pixel_columns,
                                                            parameters.late_dark_pixel_columns,
                                                            parameters.final_dark_pixel_rows,
                                                            parameters.smear_rows,
                                                            index),
                         numpy.hsplit(header_data_unit_list[0].data, parameters.number_of_slices),
                         range(parameters.number_of_slices))),
        fits_metadata=FITSMetaData(origin_file_name=origin_file_name,
                                   header=header_data_unit_list[0].header),
        parameters=parameters,
        flags=flags,
    )


def electron_flux_converter_from_fits(input_file, flags=None, parameters=None):
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
    return electron_flux_converter_from_hdulist(header_data_unit_list,
                                                origin_file_name=origin_file_name,
                                                flags=flags,
                                                parameters=parameters)
