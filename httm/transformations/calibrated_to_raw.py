"""
Transformation functions for processing a :py:class:`~httm.data_structures.RAWTransformation` so that it is suitable
for writing to a raw FITS file.
"""

import numpy

from constants import FPE_MAX_ADU
from ..data_structures import Slice


def simulate_undershoot(row, undershoot):
    """
    Simulate undershoot for one row.

    This convolves the kernel :math:`\\langle 1, -\\mathtt{undershoot}  \\rangle` with the input row,
    yielding an output row of the same length. The convolution is non-cyclic: the input row is implicitly
    padded with zero at the start to make this true. This simulates the slight "memory" the focal plane electronics
    exhibit for the signal in the previous pixel.

    :param row: Full slice image row including all pixels dark and illuminated. Units: electrons
    :type row: :py:class:`numpy.ndarray`
    :param undershoot: Undershoot parameter from parameter structure, typically ~0.001, dimensionless
    :type undershoot: float
    :rtype: :py:class:`numpy.ndarray`
    """
    kernel = numpy.array([1.0, -undershoot])
    return numpy.convolve(row, kernel, mode='same')


def convert_slice_electrons_to_adu(compression, number_of_exposures, video_scale, baseline_adu, image_slice):
    """
    TODO

    :param compression: TODO
    :type compression: float
    :param number_of_exposures: The number of exposures the image comprises.\
    This is read from the `NREADS` header of the input FITS file. TODO: Link to header description
    :type number_of_exposures: int
    :param video_scale: TODO
    :type video_scale: float
    :param baseline_adu: TODO
    :type baseline_adu: float
    :param image_slice: TODO
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
    baseline_adu = calibrated_transformation.parameters.baseline_adu
    assert len(video_scales) == len(image_slices), "Video scales do not match image slices"
    return calibrated_transformation._replace(
        slices=tuple(
            convert_slice_electrons_to_adu(
                compression,
                number_of_exposures,
                video_scale,
                image_slice,
                baseline_adu)
            for (video_scale, image_slice) in zip(video_scales, image_slices)))
