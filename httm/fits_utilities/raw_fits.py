"""
``httm.fits_utilities.raw_fits``
================================

This module contains functions for marshalling and de-marshalling
:py:class:`~httm.data_structures.raw_converter.RAWConverter` and the other book-keeping objects
it contains from a FITS file or :py:class:`astropy.io.fits.HDUList`.
"""

import numpy
from astropy.io.fits import HDUList, PrimaryHDU

from ..data_structures.raw_converter import RAWConverterFlags, RAWConverter, raw_transformation_flags, \
    RAWConverterParameters, raw_converter_parameters
from ..data_structures.common import Slice, FITSMetaData
from ..data_structures.documentation import document_parameters


def write_RAW_HDUList(converter):
    # type: (RAWConverter) -> HDUList
    # noinspection PyTypeChecker
    # TODO: Put dark pixels and smear rows where they belong
    return HDUList(PrimaryHDU(header=converter.fits_metadata.header,
                              data=numpy.hstack([raw_slice.pixels
                                                 for raw_slice in converter.slices])))


def write_RAW_fits(converter, output_file):
    # type: (RAWConverter, str) -> NoneType
    """
    Write a completed :py:class:`~httm.data_structures.raw_converter.RAWConverter` to a (simulated) raw FITS file

    :param converter:
    :type converter: :py:class:`~httm.data_structures.raw_converter.RAWConverter`
    :param output_file:
    :type output_file: :py:class:`file` or :py:class:`str`
    :rtype: NoneType
    """
    write_RAW_HDUList(converter).writeto(output_file)


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


# TODO write raw_converter_from_HDUList
def raw_converter_from_HDUList():
    pass


def raw_converter_from_file(
        input_file,
        number_of_slices=raw_converter_parameters['number_of_slices']['default'],
        video_scales=raw_converter_parameters['video_scales']['default'],
        compression=raw_converter_parameters['compression']['default'],
        undershoot=raw_converter_parameters['undershoot']['default'],
        pattern_noise=raw_converter_parameters['pattern_noise']['default']):
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
