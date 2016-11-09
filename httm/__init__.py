"""
``httm``
========

This module contains top level transformations for converting calibrated
or raw TESS full frame FITS images between one another.
"""

import numpy

from data_structures.calibrated_converter import calibrated_converter_parameters, CalibratedConverterParameters, \
    calibrated_transformation_flags, CalibratedConverterFlags, CalibratedConverter
from data_structures.documentation import document_parameters
from data_structures.raw_converter import raw_converter_parameters, RAWConverterParameters, RAWConverterFlags, \
    RAWConverter, raw_transformation_flags
from data_structures.common import Slice, FITSMetaData


# TODO: Deal with raw converter
def write_fits(output_file, calibrated_transform):
    # type: (str, CalibratedConverter) -> NoneType
    """
    Write a completed :py:class:`~httm.data_structures.calibrated_converter.CalibratedConverter` to a (simulated) raw FITS file

    :param output_file:
    :type output_file: str
    :param calibrated_transform:
    :type calibrated_transform: :py:class:`~httm.data_structures.calibrated_converter.CalibratedConverter`
    :rtype: NoneType
    """
    from astropy.io.fits import HDUList, PrimaryHDU
    from numpy import hstack
    # noinspection PyTypeChecker
    HDUList(PrimaryHDU(header=calibrated_transform.fits_metadata.header,
                       data=hstack([raw_slice.pixels
                                    for raw_slice in calibrated_transform.slices]))) \
        .writeto(output_file)


def make_slice_from_calibrated_data(pixels, index):
    # type: (numpy.ndarray, int) -> Slice
    """
    Construct a slice from an array of calibrated pixel data given a specified index.

    Result is in *electron* counts.

    :param pixels: Image pixels from the calibrated data.
    :type pixels: :py:class:`numpy.ndarray`
    :param index: The index of the slice to construct.
    :type index: int
    :rtype: :py:class:`~httm.data_structures.common.Slice`
    """
    # TODO: Add in smear and dark pixels
    image_smear_and_dark_pixels = numpy.vstack([pixels, numpy.zeros((20, pixels.shape[1]))])
    row_count = image_smear_and_dark_pixels.shape[0]
    dark_pixel_columns = numpy.zeros((row_count, 11))
    return Slice(pixels=numpy.hstack([dark_pixel_columns, image_smear_and_dark_pixels, dark_pixel_columns]),
                 index=index,
                 units='electrons')


def calibrated_converter_flags_from_file(input_file):
    """
    Construct a :py:class:`~httm.data_structures.calibrated_converter.CalibratedConverterFlags`
    from a file or file name.

    :param input_file: The file or file name to input
    :type input_file: :py:class:`file` or :py:class:`str`
    :rtype: :py:class:`~httm.data_structures.calibrated_converter.CalibratedConverter`
    """
    # TODO try to read these from file
    smear_rows_present = calibrated_transformation_flags['smear_rows_present']['default']
    readout_noise_added = calibrated_transformation_flags['readout_noise_added']['default']
    shot_noise_added = calibrated_transformation_flags['shot_noise_added']['default']
    blooming_simulated = calibrated_transformation_flags['blooming_simulated']['default']
    undershoot_uncompensated = calibrated_transformation_flags['undershoot_uncompensated']['default']
    pattern_noise_uncompensated = calibrated_transformation_flags['pattern_noise_uncompensated']['default']
    start_of_line_ringing_uncompensated = calibrated_transformation_flags['start_of_line_ringing_uncompensated'][
        'default']
    return CalibratedConverterFlags(
        smear_rows_present=smear_rows_present,
        readout_noise_added=readout_noise_added,
        shot_noise_added=shot_noise_added,
        blooming_simulated=blooming_simulated,
        undershoot_uncompensated=undershoot_uncompensated,
        pattern_noise_uncompensated=pattern_noise_uncompensated,
        start_of_line_ringing_uncompensated=start_of_line_ringing_uncompensated,
    )


def calibrated_converter_from_file(
        input_file,
        number_of_slices=calibrated_converter_parameters['number_of_slices']['default'],
        video_scales=calibrated_converter_parameters['video_scales']['default'],
        readout_noise=calibrated_converter_parameters['readout_noise']['default'],
        left_dark_pixel_columns=calibrated_converter_parameters['left_dark_pixel_columns']['default'],
        right_dark_pixel_columns=calibrated_converter_parameters['right_dark_pixel_columns']['default'],
        top_dark_pixel_rows=calibrated_converter_parameters['top_dark_pixel_rows']['default'],
        smear_rows=calibrated_converter_parameters['smear_rows']['default'],
        random_seed=calibrated_converter_parameters['random_seed']['default'],
        full_well=calibrated_converter_parameters['full_well']['default'],
        compression=calibrated_converter_parameters['compression']['default'],
        undershoot=calibrated_converter_parameters['undershoot']['default'],
        baseline_adu=calibrated_converter_parameters['baseline_adu']['default'],
        drift_adu=calibrated_converter_parameters['drift_adu']['default'],
        smear_ratio=calibrated_converter_parameters['smear_ratio']['default'],
        clip_level_adu=calibrated_converter_parameters['clip_level_adu']['default'],
        start_of_line_ringing=calibrated_converter_parameters['start_of_line_ringing']['default'],
        pattern_noise=calibrated_converter_parameters['pattern_noise']['default'],
        blooming_threshold=calibrated_converter_parameters['blooming_threshold']['default'],
):
    from astropy.io import fits
    from numpy import hsplit
    header_data_unit_list = fits.open(input_file)
    assert len(header_data_unit_list) == 1, "Only a single image per FITS file is supported"
    assert header_data_unit_list[0].data.shape[1] % number_of_slices == 0, \
        "Image did not have the specified number of slices"
    origin_file_name = None
    if isinstance(input_file, str):
        origin_file_name = input_file
    if hasattr(input_file, 'name'):
        origin_file_name = input_file.name
    return CalibratedConverter(
        slices=map(lambda pixel_data, index:
                   make_slice_from_calibrated_data(pixel_data, index),
                   hsplit(header_data_unit_list[0].data, number_of_slices),
                   range(number_of_slices)),
        fits_metadata=FITSMetaData(origin_file_name=origin_file_name,
                                   header=header_data_unit_list[0].header),
        parameters=CalibratedConverterParameters(
            number_of_slices=number_of_slices,
            video_scales=video_scales,
            readout_noise=readout_noise,
            left_dark_pixel_columns=left_dark_pixel_columns,
            right_dark_pixel_columns=right_dark_pixel_columns,
            top_dark_pixel_rows=top_dark_pixel_rows,
            smear_rows=smear_rows,
            random_seed=random_seed,
            full_well=full_well,
            compression=compression,
            undershoot=undershoot,
            baseline_adu=baseline_adu,
            drift_adu=drift_adu,
            smear_ratio=smear_ratio,
            clip_level_adu=clip_level_adu,
            start_of_line_ringing=start_of_line_ringing,
            pattern_noise=pattern_noise,
            blooming_threshold=blooming_threshold,
        ),
        flags=calibrated_converter_flags_from_file(input_file),
    )


calibrated_converter_from_file.__doc__ = """
Construct a :py:class:`~httm.data_structures.calibrated_converter.CalibratedConverter` from a file or file name

:param input_file: The file or file name to input
:type input_file: :py:class:`file` or :py:class:`str`
{parameter_documentation}
:rtype: :py:class:`~httm.data_structures.calibrated_converter.CalibratedConverter`
""".format(parameter_documentation=document_parameters(calibrated_converter_parameters))


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
        units='adu')


# TODO: Broken
def raw_converter_flags_from_file(input_file):
    """
    Construct a :py:class:`~httm.data_structures.raw_converter.RAWConverterFlags`
    from a file or file name.

    :param input_file: The file or file name to input
    :type input_file: :py:class:`file` or :py:class:`str`
    :rtype: :py:class:`~httm.data_structures.raw_converter.RAWConverterFlags`
    """
    # TODO try to read these from file
    smear_rows_present = raw_transformation_flags['smear_rows_present']['default']
    undershoot_uncompensated = raw_transformation_flags['undershoot_uncompensated']['default']
    pattern_noise_uncompensated = raw_transformation_flags['pattern_noise_uncompensated']['default']
    start_of_line_ringing_uncompensated = raw_transformation_flags['start_of_line_ringing_uncompensated'][
        'default']
    return RAWConverterFlags(
        smear_rows_present=smear_rows_present,
        undershoot_uncompensated=undershoot_uncompensated,
        pattern_noise_uncompensated=pattern_noise_uncompensated,
        start_of_line_ringing_uncompensated=start_of_line_ringing_uncompensated,
    )


def raw_converter_from_file(
        input_file,
        number_of_slices=calibrated_converter_parameters['number_of_slices']['default'],
        video_scales=calibrated_converter_parameters['video_scales']['default'],
        compression=calibrated_converter_parameters['compression']['default'],
        undershoot=calibrated_converter_parameters['undershoot']['default'],
        pattern_noise=calibrated_converter_parameters['pattern_noise']['default']):
    from astropy.io import fits
    from numpy import hsplit, fliplr
    header_data_unit_list = fits.open(input_file)
    assert len(header_data_unit_list) == 1, "Only a single image per FITS file is supported"
    assert header_data_unit_list[0].data.shape[1] % number_of_slices == 0, \
        "Image did not have the specified number of slices"
    origin_file_name = None
    if isinstance(input_file, str):
        origin_file_name = input_file
    if hasattr(input_file, 'name'):
        origin_file_name = input_file.name

    sliced_image_smear_and_dark_pixels = hsplit(header_data_unit_list[0].data[:, 44:-44], number_of_slices)

    # TODO: Document this in layout.rst
    # Rows in odd numbered slices have to be reversed
    for i in range(1, number_of_slices, 2):
        sliced_image_smear_and_dark_pixels[i] = fliplr(sliced_image_smear_and_dark_pixels[i])

    # Note that left and right dark pixels do not need to be reversed
    sliced_left_dark_pixels = hsplit(header_data_unit_list[0].data[:, :44], number_of_slices)
    sliced_right_dark_pixels = hsplit(header_data_unit_list[0].data[:, -44:], number_of_slices)

    return RAWConverter(
        slices=map(make_slice_from_raw_data,
                   sliced_image_smear_and_dark_pixels,
                   range(number_of_slices),
                   sliced_left_dark_pixels,
                   sliced_right_dark_pixels),
        fits_metadata=FITSMetaData(origin_file_name=origin_file_name,
                                   header=header_data_unit_list[0].header),
        parameters=RAWConverterParameters(
            video_scales=video_scales,
            number_of_slices=number_of_slices,
            compression=compression,
            undershoot=undershoot,
            pattern_noise=pattern_noise,
        ),
        # TODO: Read this from a file
        flags=raw_converter_flags_from_file(input_file),
    )


raw_converter_from_file.__doc__ = """
Construct a :py:class:`~httm.data_structures.raw_converter.RAWConverter` from a file or file name

:param input_file: The file or file name to input
:type input_file: :py:class:`File` or :py:class:`str`
{parameter_documentation}
:rtype: :py:class:`~httm.data_structures.raw_converter.RAWConverter`
""".format(parameter_documentation=document_parameters(raw_converter_parameters))
