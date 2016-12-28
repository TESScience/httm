"""
``httm.fits_utilities.electron_flux_fits``
==========================================

This module contains functions for marshalling and de-marshalling
:py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`
and the other book-keeping objects it contains to and from FITS files or :py:class:`astropy.io.fits.HDUList` objects.
"""

import os

import astropy
import numpy
from astropy.io.fits import HDUList, PrimaryHDU

from .header_settings import get_header_setting
from ..data_structures.common import Slice, FITSMetaData
from ..data_structures.electron_flux_converter import \
    SingleCCDElectronFluxConverterFlags, SingleCCDElectronFluxConverterParameters, \
    SingleCCDElectronFluxConverter, electron_flux_transformation_flags, electron_flux_converter_parameters


# TODO: Documentation
def make_slice_from_electron_flux_data(
        pixels,
        early_dark_pixel_columns,
        late_dark_pixel_columns,
        final_dark_pixel_rows,
        smear_rows,
        index):
    # type: (numpy.ndarray, int, int, int, int, int) -> Slice
    """
    Construct a slice from an array of electron flux pixel data given a specified index.

    Result is in *electron* counts.

    :param pixels: Image pixels from the electron flux data
    :type pixels: :py:class:`numpy.ndarray`
    :param early_dark_pixel_columns:
    :type early_dark_pixel_columns: int
    :param late_dark_pixel_columns:
    :type late_dark_pixel_columns: int
    :param final_dark_pixel_rows:
    :type final_dark_pixel_rows: int
    :param smear_rows:
    :type smear_rows: int
    :param index: The index of the slice to construct
    :type index: int
    :rtype: :py:class:`~httm.data_structures.common.Slice`
    """
    image_and_smear_and_final_dark_pixels = numpy.vstack(
        [pixels, numpy.zeros((final_dark_pixel_rows + smear_rows, pixels.shape[1]))])
    row_count = image_and_smear_and_final_dark_pixels.shape[0]
    early_dark_pixels = numpy.zeros((row_count, early_dark_pixel_columns))
    late_dark_pixels = numpy.zeros((row_count, late_dark_pixel_columns))
    return Slice(
        pixels=numpy.hstack([early_dark_pixels, image_and_smear_and_final_dark_pixels, late_dark_pixels]),
        index=index,
        units='electrons',
    )


# TODO: Documentation
def electron_flux_converter_flags_from_fits_header(fits_header, flag_overrides=None):
    """
    Construct a :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverterFlags`
    from a file or file name.

    :param fits_header: The file or file name to input
    :type fits_header: :py:class:`astropy.io.fits.Header`
    :param flag_overrides:
    :type flag_overrides: object
    :rtype: :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverterFlags`
    """

    def get_flag(flag_name):
        return get_header_setting(
            flag_name,
            electron_flux_transformation_flags,
            fits_header,
            getattr(flag_overrides, flag_name) if hasattr(flag_overrides, flag_name) else None)

    return SingleCCDElectronFluxConverterFlags(
        smear_rows_present=get_flag('smear_rows_present'),
        readout_noise_present=get_flag('readout_noise_present'),
        shot_noise_present=get_flag('shot_noise_present'),
        blooming_present=get_flag('blooming_present'),
        undershoot_present=get_flag('undershoot_present'),
        pattern_noise_present=get_flag('pattern_noise_present'),
        start_of_line_ringing_present=get_flag('start_of_line_ringing_present'),
        baseline_present=get_flag('baseline_present'),
        in_adu=get_flag('in_adu'),
    )


# TODO: Documentation
def electron_flux_converter_parameters_from_fits_header(fits_header, parameter_overrides=None):
    """
    TODO: Document me

    :param fits_header: FITS header to use for parsing parameters
    :type fits_header: :py:class:`astropy.io.fits.Header`
    :param parameter_overrides:
    :type parameter_overrides: object
    :return:
    """

    def get_parameter(parameter_name):
        return get_header_setting(
            parameter_name,
            electron_flux_converter_parameters,
            fits_header,
            getattr(parameter_overrides, parameter_name) if hasattr(parameter_overrides, parameter_name) else None)

    return SingleCCDElectronFluxConverterParameters(
        number_of_slices=get_parameter('number_of_slices'),
        camera_number=get_parameter('camera_number'),
        ccd_number=get_parameter('ccd_number'),
        number_of_exposures=get_parameter('number_of_exposures'),
        video_scales=get_parameter('video_scales'),
        readout_noise_parameters=get_parameter('readout_noise_parameters'),
        early_dark_pixel_columns=get_parameter('early_dark_pixel_columns'),
        late_dark_pixel_columns=get_parameter('late_dark_pixel_columns'),
        final_dark_pixel_rows=get_parameter('final_dark_pixel_rows'),
        smear_rows=get_parameter('smear_rows'),
        random_seed=get_parameter('random_seed'),
        full_well=get_parameter('full_well'),
        gain_loss=get_parameter('gain_loss'),
        undershoot_parameter=get_parameter('undershoot_parameter'),
        single_frame_baseline_adus=get_parameter('single_frame_baseline_adus'),
        single_frame_baseline_adu_drift_term=get_parameter('single_frame_baseline_adu_drift_term'),
        smear_ratio=get_parameter('smear_ratio'),
        clip_level_adu=get_parameter('clip_level_adu'),
        start_of_line_ringing=get_parameter('start_of_line_ringing'),
        pattern_noise=get_parameter('pattern_noise'),
        blooming_threshold=get_parameter('blooming_threshold'),
    )


# TODO: Write flags and parameters to hdulist
def electron_flux_converter_to_simulated_raw_hdulist(converter):
    # type: (SingleCCDElectronFluxConverter) -> HDUList
    """
    This function converts a :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`
    into an :py:class:`astropy.io.fits.HDUList` object, suitable for writing out to a simulated raw FITS file.

    :param converter: An electron flux converter object
    :type converter: :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`
    :rtype: :py:class:`astropy.io.fits.HDUList`
    """

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


# TODO: Documentation
def write_electron_flux_converter_to_simulated_raw_fits(converter, output_file):
    # type: (SingleCCDElectronFluxConverter, str) -> None
    """
    Write a :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`
    to a simulated raw FITS file.

    :param converter:
    :type converter: :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter`
    :param output_file:
    :type output_file: str
    :rtype: NoneType
    """
    hdulist = electron_flux_converter_to_simulated_raw_hdulist(converter)

    try:
        os.remove(output_file)
    except OSError:
        pass

    hdulist.writeto(output_file)


# TODO: Documentation
# noinspection PyUnresolvedReferences
def electron_flux_converter_from_hdulist(header_data_unit_list, origin_file_name=None,
                                         flag_overrides=None, parameter_overrides=None):
    """
    TODO: Document me

    :param header_data_unit_list:
    :param origin_file_name:
    :param flag_overrides:
    :param parameter_overrides:
    :return:
    """
    fits_metadata = FITSMetaData(origin_file_name=origin_file_name,
                                 header=header_data_unit_list[0].header)  # type: FITSMetaData
    flag_overrides = electron_flux_converter_flags_from_fits_header(fits_metadata.header,
                                                                    flag_overrides=flag_overrides)
    parameter_overrides = electron_flux_converter_parameters_from_fits_header(fits_metadata.header,
                                                                              parameter_overrides=parameter_overrides)
    assert len(header_data_unit_list) == 1, "Only a single image per FITS file is supported"
    assert header_data_unit_list[0].data.shape[1] % parameter_overrides.number_of_slices == 0, \
        "Image did not have the specified number of slices"
    return SingleCCDElectronFluxConverter(
        slices=tuple(map(lambda pixel_data, index:
                         make_slice_from_electron_flux_data(pixel_data,
                                                            parameter_overrides.early_dark_pixel_columns,
                                                            parameter_overrides.late_dark_pixel_columns,
                                                            parameter_overrides.final_dark_pixel_rows,
                                                            parameter_overrides.smear_rows,
                                                            index),
                         numpy.hsplit(header_data_unit_list[0].data, parameter_overrides.number_of_slices),
                         range(parameter_overrides.number_of_slices))),
        fits_metadata=fits_metadata,
        parameters=parameter_overrides,
        flags=flag_overrides,
    )


# TODO: Documentation
def electron_flux_converter_from_fits(input_file, flag_overrides=None, parameter_overrides=None):
    """
    TODO: Document me

    :param input_file:
    :param flag_overrides:
    :param parameter_overrides:
    :return:
    """
    origin_file_name = None
    if isinstance(input_file, str):
        origin_file_name = input_file
    if hasattr(input_file, 'name'):
        origin_file_name = input_file.name
    if origin_file_name:
        header_data_unit_list = astropy.io.fits.open(origin_file_name)
    elif isinstance(input_file, astropy.io.fits.HDUList):
        header_data_unit_list = input_file
    else:
        raise RuntimeError("Cannot make HDU for object of type {}".format(str(type(input_file))))
    return electron_flux_converter_from_hdulist(
        header_data_unit_list,
        origin_file_name=origin_file_name,
        flag_overrides=flag_overrides,
        parameter_overrides=parameter_overrides,
    )
