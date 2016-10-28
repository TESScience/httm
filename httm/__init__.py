"""
`httm` contains top level transformations for
converting calibrates or raw TESS full Frame FITS images between one another.


"""


# See https://docs.python.org/2/library/collections.html#collections.namedtuple for details
import numpy

# The maximum number of Analogue to Digital Converter Units a pixel can contain
from httm.data_structures import Slice, CalibratedTransformation, CalibratedTransformParameters, FITSMetaData, \
    RAWTransformation, RAWTransformParameters

FPE_MAX_ADU = 65535


def write_calibrated_fits(output_file, raw_transform):
    """
    Write a completed :py:class:`~httm.data_structures.RAWTransformation` to a calibrated FITS file

    :param output_file:
    :type output_file: str
    :param raw_transform:
    :type raw_transform: :py:class:`~httm.data_structures.RAWTransformation`
    :rtype: NoneType
    """
    from astropy.io.fits import HDUList, PrimaryHDU
    from numpy import hstack
    print raw_transform
    # noinspection PyTypeChecker
    HDUList(PrimaryHDU(header=raw_transform.fits_metadata.header,
                       data=hstack([calibrated_slice.image_pixels
                                    for calibrated_slice in raw_transform.slices]))) \
        .writeto(output_file)


def convert_slice_electrons_to_adu(compression, number_of_exposures, video_scale, baseline_adu, image_slice):
    """
    TODO

    :type number_of_exposures: int
    :param compression:
    :type compression: float
    :param number_of_exposures:
    :type number_of_exposures: int
    :param video_scale:
    :type video_scale: float
    :param baseline_adu:
    :type baseline_adu: float
    :param image_slice:
    :type image_slice: :py:class:`~httm.data_structures.Slice`
    :rtype: :py:class:`~httm.data_structures.Slice`
    """
    assert image_slice.units == "electrons", "units must be electrons"
    compression_per_adu = compression / (number_of_exposures * FPE_MAX_ADU)  # type: float
    compression_per_electron = compression_per_adu / video_scale  # type: float
    exposure_baseline = baseline_adu * number_of_exposures

    def transform_electron_to_adu(electron):
        return exposure_baseline + electron / (video_scale * (1.0 + compression_per_electron * electron))

    return Slice(smear_rows=transform_electron_to_adu(image_slice.smear_rows),
                 top_dark_pixel_rows=transform_electron_to_adu(image_slice.top_dark_pixel_rows),
                 left_dark_pixel_columns=transform_electron_to_adu(image_slice.left_dark_pixel_columns),
                 right_dark_pixel_columns=transform_electron_to_adu(image_slice.right_dark_pixel_columns),
                 index=image_slice.index,
                 units="ADU",
                 image_pixels=transform_electron_to_adu(image_slice.image_pixels))


def convert_slice_adu_to_electrons(compression, number_of_exposures, video_scale, image_slice):
    """
    TODO

    :param compression:
    :type compression: float
    :param number_of_exposures:
    :type number_of_exposures: int
    :param video_scale:
    :type video_scale: float
    :param image_slice:
    :type image_slice: :py:class:`~httm.data_structures.Slice`
    :rtype: :py:class:`~httm.data_structures.Slice`
    """
    assert image_slice.units == "ADU", "units must be ADU"
    compression_per_adu = compression / (number_of_exposures * FPE_MAX_ADU)  # type: float
    compression_per_electron = compression_per_adu / video_scale  # type: float

    def transform_adu_to_electron(adu):
        return adu / (-1.0 / video_scale + compression_per_electron * adu)

    return Slice(smear_rows=transform_adu_to_electron(image_slice.smear_rows),
                 top_dark_pixel_rows=transform_adu_to_electron(image_slice.top_dark_pixel_rows),
                 left_dark_pixel_columns=transform_adu_to_electron(image_slice.left_dark_pixel_columns),
                 right_dark_pixel_columns=transform_adu_to_electron(image_slice.right_dark_pixel_columns),
                 index=image_slice.index,
                 units="electrons",
                 image_pixels=transform_adu_to_electron(image_slice.image_pixels))


# noinspection PyProtectedMember
def convert_electrons_to_adu(calibrated_transformation):
    """
    Converts a :py:class:`~httm.data_structures.CalibratedTransformation` from having electrons
    to *Analogue to Digital Converter Units* (ADU).

    :param calibrated_transformation: Should have electrons for units
    :type calibrated_transformation: :py:class:`~httm.data_structures.CalibratedTransformation`
    :rtype: :py:class:`~httm.data_structures.CalibratedTransformation`
    """
    video_scales = calibrated_transformation.parameters.video_scales
    image_slices = calibrated_transformation.slices
    number_of_exposures = calibrated_transformation.fits_metadata.header['NREADS']
    compression = calibrated_transformation.parameters.compression
    assert len(video_scales) == len(image_slices), "Video scales do not match image slices"
    return calibrated_transformation._replace(
        slices=tuple(
            convert_slice_electrons_to_adu(
                compression,
                number_of_exposures,
                video_scale,
                image_slice)
            for (video_scale, image_slice) in zip(video_scales, image_slices)))


# noinspection PyProtectedMember
def convert_adu_to_electrons(raw_transformation):
    """
    Converts a :py:class:`~httm.data_structures.RAWTransformation` from
    having *Analogue to Digital Converter Units* (ADU) to electron counts.

    :param raw_transformation: Should have electrons for units
    :type raw_transformation: :py:class:`~httm.data_structures.RAWTransformation`
    :rtype: :py:class:`~httm.data_structures.RAWTransformation`
    """
    video_scales = raw_transformation.parameters.video_scales
    image_slices = raw_transformation.slices
    number_of_exposures = raw_transformation.fits_metadata.header['NREADS']
    compression = raw_transformation.parameters.compression
    assert len(video_scales) == len(image_slices), "Video scales do not match image slices"
    return raw_transformation._replace(
        slices=tuple(
            convert_slice_adu_to_electrons(
                compression,
                number_of_exposures,
                video_scale,
                image_slice)
            for (video_scale, image_slice) in zip(video_scales, image_slices)))


def write_raw_fits(output_file, calibrated_transform):
    """
    Write a completed :py:class:`~httm.data_structures.CalibratedTransformation` to a (simulated) raw FITS file

    :param output_file:
    :type output_file: str
    :param calibrated_transform:
    :type calibrated_transform: :py:class:`~httm.data_structures.CalibratedTransformation`
    :rtype: NoneType
    """
    from astropy.io.fits import HDUList, PrimaryHDU
    from numpy import hstack
    # noinspection PyTypeChecker
    HDUList(PrimaryHDU(header=calibrated_transform.fits_metadata.header,
                       data=hstack([raw_slice.image_pixels
                                    for raw_slice in calibrated_transform.slices]))) \
        .writeto(output_file)


def make_slice_from_calibrated_data(image_pixels, index):
    """
    Construct a slice from an array of calibrated pixel data given a specified index

    :param image_pixels: Image pixels from the calibrated data
    :type image_pixels: :py:class:`numpy.ndarray`
    :param index: The index of the slice to construct
    :type index: int
    :rtype: :py:class:`~httm.data_structures.Slice`
    """
    return Slice(image_pixels=image_pixels,
                 index=index,
                 units='electrons')


def calibrated_transform_from_file(input_file, number_of_slices=4, **kwargs):
    """
    Construct a :py:class:`~httm.data_structures.CalibratedTransformation` from a file or file name

    :param input_file: The file or file name to input
    :param number_of_slices: The numbers of slices
    :type input_file: :py:class:`File` or :py:class:`str`
    :rtype: :py:class:`~httm.data_structures.CalibratedTransformation`
    """
    from astropy.io import fits
    from numpy import hsplit
    header_data_unit_list = fits.open(input_file)
    assert len(header_data_unit_list) == 1, "Only a single image per FITS file is supported"
    assert header_data_unit_list[0].data.shape[1] % number_of_slices == 0, \
        "Image did not have the specified number of slices"
    origin_file_name = None
    if isinstance(input_file, basestring):
        origin_file_name = input_file
    if hasattr(input_file, 'name'):
        origin_file_name = input_file.name
    return CalibratedTransformation(
        slices=map(lambda pixel_data, index:
                   make_slice_from_calibrated_data(pixel_data, index),
                   hsplit(header_data_unit_list[0].data, number_of_slices),
                   range(number_of_slices)),
        fits_metadata=FITSMetaData(origin_file_name=origin_file_name,
                                   header=header_data_unit_list[0].header),
        parameters=CalibratedTransformParameters(number_of_slices=number_of_slices, **kwargs))


def raw_transform_from_file(input_file, number_of_slices=4, **kwargs):
    """
    Construct a :py:class:`~httm.data_structures.RAWTransformation` from a file or file name

    :param number_of_slices:
    :type number_of_slices: int
    :param input_file: The file or file name to input
    :type input_file: :py:class:`File` or :py:class:`str`
    :rtype: :py:class:`~httm.data_structures.RAWTransformation`
    """
    from astropy.io import fits
    from numpy import hsplit, vsplit
    header_data_unit_list = fits.open(input_file)
    assert len(header_data_unit_list) == 1, "Only a single image per FITS file is supported"
    assert header_data_unit_list[0].data.shape[1] % number_of_slices == 0, \
        "Image did not have the specified number of slices"
    origin_file_name = None
    if isinstance(input_file, basestring):
        origin_file_name = input_file
    if hasattr(input_file, 'name'):
        origin_file_name = input_file.name

    sliced_image_pixels = hsplit(header_data_unit_list[0].data[20:, 44:-44], number_of_slices)
    sliced_left_dark_pixels = vsplit(header_data_unit_list[0].data[:, :44], number_of_slices)
    sliced_right_dark_pixels = vsplit(header_data_unit_list[0].data[:, -44:], number_of_slices)
    sliced_top_dark_pixels = hsplit(header_data_unit_list[0].data[:10, 44:-44], number_of_slices)
    sliced_smear_rows = hsplit(header_data_unit_list[0].data[10:20, 44:-44], number_of_slices)
    # TODO: Factor me out
    make_raw_pixel_slice = lambda image_pixels, index, left_dark_pixel_columns, right_dark_pixel_columns, top_dark_pixel_rows, smear_rows: Slice(
        image_pixels=image_pixels,
        index=index,
        left_dark_pixel_columns=left_dark_pixel_columns,
        right_dark_pixel_columns=right_dark_pixel_columns,
        top_dark_pixel_rows=top_dark_pixel_rows,
        smear_rows=smear_rows,
        units='hdu')
    return RAWTransformation(
        slices=map(make_raw_pixel_slice,
                   sliced_image_pixels,
                   range(number_of_slices),
                   sliced_left_dark_pixels,
                   sliced_right_dark_pixels,
                   sliced_top_dark_pixels,
                   sliced_smear_rows),
        fits_metadata=FITSMetaData(origin_file_name=origin_file_name,
                                   header=header_data_unit_list[0].header),
        parameters=RAWTransformParameters(number_of_slices=number_of_slices, **kwargs))
