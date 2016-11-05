"""
``httm.transformations.raw_to_calibrated``
==========================================

This module contains transformation functions for processing
a :py:class:`~httm.data_structures.raw_converter.RAWConverter` so that it is suitable for
writing to a calibrated FITS file.
"""
import numpy

from constants import FPE_MAX_ADU
from ..data_structures.common import Slice


def remove_start_of_line_ringing_from_slice(image_slice):
    # type: (Slice) -> Slice
    pass


def remove_smear_from_slice(image_slice):
    # type: (Slice) -> Slice
    pass


def remove_pattern_noise_from_slice(pattern_noise, image_slice):
    # type: (numpy.ndarray, Slice) -> Slice
    pass


def remove_undershoot_from_row(row, undershoot):
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
    :type image_slice: :py:class:`~httm.data_structures.common.Slice`
    :rtype: :py:class:`~httm.data_structures.common.Slice`
    """
    assert image_slice.units == "ADU", "units must be ADU"
    compression_per_adu = compression / (number_of_exposures * FPE_MAX_ADU)  # type: float
    compression_per_electron = compression_per_adu / video_scale  # type: float

    def transform_adu_to_electron(adu):
        # type: (float) -> float
        return adu / (-1.0 / video_scale + compression_per_electron * adu)

    return Slice(index=image_slice.index,
                 units="electrons",
                 pixels=transform_adu_to_electron(image_slice.pixels))


# noinspection PyProtectedMember
def convert_adu_to_electrons(raw_transformation):
    # type: (RAWConverter) -> RAWConverter
    """
    Converts a :py:class:`~httm.data_structures.raw_converter.RAWConverter` from
    having *Analogue to Digital Converter Units* (ADU) to electron counts.

    :param raw_transformation: Should have electrons for units
    :type raw_transformation: :py:class:`~httm.data_structures.raw_converter.RAWConverter`
    :rtype: :py:class:`~httm.data_structures.raw_converter.RAWConverter`
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
