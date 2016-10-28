"""
Transformation functions for processing a :py:class:`~httm.data_structures.RAWTransformation` so that it is suitable
for writing to a calibrated FITS file.
"""
import numpy

from constants import FPE_MAX_ADU
from ..data_structures import Slice, RAWTransformation


def remove_undershoot(row, undershoot):
    # type: (numpy.ndarray, float) -> numpy.ndarray
    """
    Remove undershoot from one row.

    This convolves the kernel :math:`\\langle 1, \\mathtt{undershoot}  \\rangle` with the input row,
    yielding an output row of the same length. The convolution is non-cyclic: the input row is implicitly
    padded with zero at the start to make this true. This undoes the slight "memory" the focal plane electronics
    exhibit for the signal in the previous pixel.

    :param row: Full slice image row including all pixels dark and illuminated. Units: electrons
    :type row: :py:class:`numpy.ndarray`
    :param undershoot: Undershoot parameter from parameter structure, typically ~0.001, dimensionless
    :type undershoot: float
    :rtype: :py:class:`numpy.ndarray`
    """
    kernel = numpy.array([1.0, undershoot])
    return numpy.convolve(row, kernel, mode='same')


def convert_slice_adu_to_electrons(compression, number_of_exposures, video_scale, image_slice):
    # type: (float, int, float, Slice) -> Slice
    """
    TODO

    :param compression: TODO
    :type compression: float
    :param number_of_exposures: The number of exposures the image comprises.\
    This is read from the `NREADS` header of the input FITS file. TODO: Link to header description
    :type number_of_exposures: int
    :param video_scale: TODO
    :type video_scale: float
    :param image_slice: TODO
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
def convert_adu_to_electrons(raw_transformation):
    # type: (RAWTransformation) -> RAWTransformation
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
