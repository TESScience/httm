"""
``httm.transformations.raw_slices_to_calibrated``
=================================================

Transformation functions for processing slices contained in a
:py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter` so that they are suitable
for writing to a calibrated FITS file.

"""
import numpy

from constants import FPE_MAX_ADU
from ..data_structures.common import Slice


def remove_start_of_line_ringing_from_slice(top_dark_pixel_rows, image_slice):
    # type: (int, Slice) -> Slice
    """
    Estimate start of line ringing from the upper dark rows and remove it from a slice.
    
    This averages the upper dark rows and subtracts the result from each row in the image.
    This will also implicitly remove the video baseline.
    This should not be necessary if you're removing smear.

    :param top_dark_pixel_rows: Number of top dark pixel rows
    :type top_dark_pixel_rows: int
    :param image_slice: Input slice. Units: electrons
    :type image_slice: :py:class:`~httm.data_structures.common.Slice`
    :rtype: :py:class:`~httm.data_structures.common.Slice`
    """
    working_pixels = image_slice.pixels
    mean_ringing = numpy.sum(working_pixels[:-top_dark_pixel_rows], 0) / top_dark_pixel_rows
    working_pixels -= mean_ringing
    # noinspection PyProtectedMember
    return image_slice._replace(pixels=working_pixels)


def remove_smear_from_slice(top_dark_pixel_rows, smear_rows, image_slice):
    # type: (int, int, Slice) -> Slice
    """
    Estimate start of line ringing from the upper dark rows and remove it from a slice.
    
    This averages the smear rows and subtracts the result from each row in the image.
    This will also implicitly remove start of line ringing and the video baseline.

    :param top_dark_pixel_rows: Number of top dark pixel rows
    :type top_dark_pixel_rows: int
    :param smear_rows: Number of smear rows
    :type smear_rows: int
    :param image_slice: Input slice. Units: electrons
    :type image_slice: :py:class:`~httm.data_structures.common.Slice`
    :rtype: :py:class:`~httm.data_structures.common.Slice`
    """
    working_pixels = image_slice.pixels
    mean_ringing = numpy.sum(
        working_pixels[-top_dark_pixel_rows:-top_dark_pixel_rows - smear_rows], 0) / smear_rows
    working_pixels -= mean_ringing
    # noinspection PyProtectedMember
    return image_slice._replace(pixels=working_pixels)


def remove_pattern_noise_from_slice(pattern_noise, image_slice):
    # type: (numpy.ndarray, Slice) -> Slice
    """
    Remove a fixed pattern from the image.
    
    :param pattern_noise: 2d array of dimensions matching the pixel array of a slice
    :type pattern_noise: :py:class:`numpy.ndarray`
    :param image_slice: Input slice. Units: electrons
    :type image_slice: :py:class:`~httm.data_structures.common.Slice`
    :rtype: :py:class:`~httm.data_structures.common.Slice`
    """
    return image_slice._replace(pixels=image_slice.pixels - pattern_noise)


def remove_undershoot_from_slice(undershoot, image_slice):
    # type: (float, Slice) -> Slice
    """
    Remove undershoot from a slice

    This convolves the kernel :math:`\\langle 1, \\mathtt{undershoot}  \\rangle` with each row,
    yielding a row of the same length. The convolution is non-cyclic: the input row is implicitly
    padded with zero at the start to make this true. This undoes the slight "memory" the focal plane electronics
    exhibit for the signal in the previous pixel.

    :param undershoot: Undershoot parameter from parameter structure, typically ~0.001, dimensionless
    :type undershoot: float
    :param image_slice: Input slice. Units: electrons
    :type image_slice: :py:class:`~httm.data_structures.common.Slice`
    :rtype: :py:class:`~httm.data_structures.common.Slice`
    """
    kernel = numpy.array([1.0, undershoot])

    def convolve_row(row):
        return numpy.convolve(row, kernel, mode='same')

    # noinspection PyProtectedMember
    return image_slice._replace(pixels=numpy.apply_along_axis(convolve_row, 1, image_slice.pixels))


# TODO: this is wrong
def convert_slice_adu_to_electrons(
        gain_loss, number_of_exposures, video_scale, image_slice):
    # type: (float, int, float, Slice) -> Slice
    """
    Converts a slice from *Analogue to Digital Converter Units* (ADU) to electron counts.

    TODO: Present math

    This function is the inverse transform of
    :py:func:`~httm.transformations.calibrated_slices_to_raw.convert_slice_electrons_to_adu`.
    Note that unlike :py:func:`~httm.transformations.calibrated_slices_to_raw.convert_slice_electrons_to_adu`,
    this function does not handle the *exposure baseline* and that is instead handled in ???.

    :param gain_loss: The relative decrease in video gain over the total ADC range
    :type gain_loss: float
    :param number_of_exposures: The number of exposures the image comprises.
    :type number_of_exposures: int
    :param video_scale: Constant for converting electron counts to \
    *Analogue to Digital Converter Units* (ADU). Units: electrons per ADU
    :type video_scale: float
    :param image_slice: Input slice. Units: electrons
    :type image_slice: :py:class:`~httm.data_structures.common.Slice`
    :rtype: :py:class:`~httm.data_structures.common.Slice`
    """
    assert image_slice.units == "ADU", "pixel units must be in ADU"
    gain_loss_per_adu = gain_loss / (number_of_exposures * FPE_MAX_ADU)  # type: float
    gain_loss_per_electron = gain_loss_per_adu / video_scale  # type: float

    def transform_adu_to_electron(adu):
        # type: (float) -> float
        return (video_scale * adu) / \
               (1 + gain_loss_per_electron * video_scale * adu)

    return Slice(index=image_slice.index,
                 units="electrons",
                 pixels=transform_adu_to_electron(image_slice.pixels))
