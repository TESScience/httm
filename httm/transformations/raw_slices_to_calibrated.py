# HTTM: A transformation library for RAW and Electron Flux TESS Images
# Copyright (C) 2016, 2017 John Doty and Matthew Wampler-Doty of Noqsi Aerospace, Ltd.
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""
``httm.transformations.raw_slices_to_calibrated``
=================================================

Transformation functions for processing slices contained in a
:py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter` so that they are suitable
for writing to a calibrated FITS file.

"""
import numpy

from .constants import FPE_MAX_ADU
from ..data_structures.common import Slice


def remove_start_of_line_ringing_from_slice(final_dark_pixel_rows, image_slice):
    # type: (int, Slice) -> Slice
    """
    This function estimates *start of line ringing* from the upper dark rows of a slice and compensates for this
    effect.
    
    This averages the upper dark rows and subtracts the result from each row in the image.

    This will also implicitly remove the video bias.

    This should not be necessary if smear is already being removed.

    :param final_dark_pixel_rows: Number of top dark pixel rows
    :type final_dark_pixel_rows: int
    :param image_slice: Input slice. Units: electrons
    :type image_slice: :py:class:`~httm.data_structures.common.Slice`
    :rtype: :py:class:`~httm.data_structures.common.Slice`
    """
    assert image_slice.units == "electrons", "units must be electrons"
    working_pixels = numpy.copy(image_slice.pixels)
    mean_ringing = numpy.sum(working_pixels[:-final_dark_pixel_rows], 0) / final_dark_pixel_rows
    working_pixels -= mean_ringing
    # noinspection PyProtectedMember
    return image_slice._replace(pixels=working_pixels)


def remove_smear_from_slice(early_dark_pixel_columns,
                            late_dark_pixel_columns,
                            final_dark_pixel_rows,
                            smear_rows,
                            image_slice):
    # type: (int, int, int, int, Slice) -> Slice
    """
    This function estimates *smear* from the *smear rows* of a slice and compensates for this
    effect.

    This averages the smear rows and subtracts the result from each row in the image.

    Smear rows are then zeroed.

    This transformation implicitly removes *start of line ringing* and the *baseline electron count*.

    :param early_dark_pixel_columns: The number of dark pixel columns on the left side of the slice
    :type early_dark_pixel_columns: int
    :param late_dark_pixel_columns: The number of dark pixel columns on the right side of the slice
    :type late_dark_pixel_columns: int
    :param final_dark_pixel_rows: The number of top dark pixel rows
    :type final_dark_pixel_rows: int
    :param smear_rows: The number of smear rows
    :type smear_rows: int
    :param image_slice: Input slice. Units: electrons
    :type image_slice: :py:class:`~httm.data_structures.common.Slice`
    :rtype: :py:class:`~httm.data_structures.common.Slice`
    """
    assert image_slice.units == "electrons", "units must be electrons"
    top = (final_dark_pixel_rows + smear_rows)
    smear_pixels = image_slice.pixels[-top:-final_dark_pixel_rows, early_dark_pixel_columns:-late_dark_pixel_columns]
    # noinspection PyTypeChecker
    assert numpy.any(smear_pixels != 0), "Smear rows should not be zero"
    working_pixels = numpy.copy(image_slice.pixels)
    mean_smear = numpy.sum(
        working_pixels[-top:-final_dark_pixel_rows], 0) / smear_rows
    working_pixels -= mean_smear
    # noinspection PyProtectedMember
    return image_slice._replace(pixels=working_pixels)


def remove_baseline_from_slice(early_dark_pixel_columns, late_dark_pixel_columns, image_slice):
    # type: (int, int, Slice) -> Slice
    """
    This function estimates *baseline* from the *dark pixels* of a slice and compensates for this
    effect.

    This averages the pixels in the dark columns and subtracts the result from each pixel in the image.

    :param early_dark_pixel_columns: The number of dark pixel columns on the left side of the slice
    :type early_dark_pixel_columns: int
    :param late_dark_pixel_columns: The number of dark pixel columns on the right side of the slice
    :type late_dark_pixel_columns: int
    :param image_slice: Input slice. Units: electrons
    :type image_slice: :py:class:`~httm.data_structures.common.Slice`
    :rtype: :py:class:`~httm.data_structures.common.Slice`
    """
    assert image_slice.units == "electrons", "units must be electrons"
    early = numpy.ravel(image_slice.pixels[:, :early_dark_pixel_columns])
    late = numpy.ravel(image_slice.pixels[:, -late_dark_pixel_columns:])
    mean = numpy.mean(numpy.concatenate((early, late)))
    # noinspection PyProtectedMember
    return image_slice._replace(pixels=image_slice.pixels - mean)


def remove_pattern_noise_from_slice(pattern_noise, image_slice):
    # type: (numpy.ndarray, Slice) -> Slice
    """
    This transformation corrects for a fixed pattern of noise on a :py:class:`~httm.data_structures.common.Slice`.

    :param pattern_noise: 2d array of dimensions matching the pixel array of a slice
    :type pattern_noise: :py:class:`numpy.ndarray`
    :param image_slice: Input slice. Units: ADU
    :type image_slice: :py:class:`~httm.data_structures.common.Slice`
    :rtype: :py:class:`~httm.data_structures.common.Slice`
    """
    assert image_slice.units == "ADU", "pixel units must be in ADU"
    # noinspection PyProtectedMember
    return image_slice._replace(pixels=image_slice.pixels - pattern_noise)


def remove_undershoot_from_slice(undershoot_parameter, image_slice):
    # type: (float, Slice) -> Slice
    """
    When a CCD reads out a bright pixel, the pixel to the right of it appears artificially dimmer.

    This is *undershoot*.

    This function compensates for this effect on a slice.

    This convolves the kernel :math:`\\langle 1, \\mathtt{undershoot\\_parameter}  \\rangle` with each row,
    yielding a row of the same length. The convolution is non-cyclic: the input row is implicitly
    padded with zero at the start to make this true. This undoes the slight "memory" the focal plane electronics
    exhibit for the signal in the previous pixel.

    This transformation is the (approximate) inverse of
    :py:func:`~httm.transformations.electron_flux_slices_to_raw.simulate_undershoot_on_slice`.

    :param undershoot_parameter: Undershoot parameter from parameter structure, typically ~0.001, dimensionless
    :type undershoot_parameter: float
    :param image_slice: Input slice. Units: electrons
    :type image_slice: :py:class:`~httm.data_structures.common.Slice`
    :rtype: :py:class:`~httm.data_structures.common.Slice`
    """
    assert image_slice.units == "electrons", "units must be electrons"
    convolutional_kernel = numpy.array([1.0, undershoot_parameter])

    def convolve_row(row):
        return numpy.convolve(row, convolutional_kernel, mode='same')

    # noinspection PyProtectedMember
    return image_slice._replace(pixels=numpy.apply_along_axis(convolve_row, 1, image_slice.pixels))


def convert_slice_adu_to_electrons(gain_loss, number_of_exposures, video_scale, image_slice):
    # type: (float, int, float, Slice) -> Slice
    """
    Converts a slice from *Analogue to Digital Converter Units* (ADU) to electron counts.

    Define the following values:

    :math:`\\displaystyle{\\mathtt{FPE\\_MAX\\_ADU} := 65535}`

    :math:`\\displaystyle{\\mathtt{gain\\_loss\\_per\\_adu} := \\frac{\\mathtt{gain\\_loss}}
    {\\mathtt{number\\_of\\_exposures}\\times\\mathtt{FPE\\_MAX\\_ADU}}}`

    :math:`\\displaystyle{\\mathtt{gain\\_loss\\_per\\_electron} := \\frac{\\mathtt{gain\\_loss\\_per\\_adu}}
    {\\mathtt{video\\_scale}}}`

    For each pixel :math:`p`, with units in ADU, this function applies the following transformation:

    :math:`\\displaystyle{\\frac{\\mathtt{video\\_scale} \\times p}{1 - \\mathtt{gain\\_loss\\_per\\_electron}
    \\times \\mathtt{video\\_scale} \\times p}}`

    This function is the inverse transform of
    :py:func:`~httm.transformations.electron_flux_slices_to_raw.convert_slice_electrons_to_adu`.

    :param gain_loss: The relative decrease in video gain over the total ADC range
    :type gain_loss: float
    :param number_of_exposures: The number of exposures the image comprises.
    :type number_of_exposures: int
    :param video_scale: Constant for converting electron counts to \
    *Analogue to Digital Converter Units* (ADU). Units: electrons per ADU
    :type video_scale: float
    :param image_slice: Input slice. Units: ADU
    :type image_slice: :py:class:`~httm.data_structures.common.Slice`
    :rtype: :py:class:`~httm.data_structures.common.Slice`
    """
    assert image_slice.units == "ADU", "pixel units must be in ADU"
    gain_loss_per_adu = gain_loss / (number_of_exposures * FPE_MAX_ADU)  # type: float
    gain_loss_per_electron = gain_loss_per_adu / video_scale  # type: float

    def transform_adu_to_electron(adu):
        # type: (float) -> float
        return (video_scale * adu) / (1 - gain_loss_per_electron * video_scale * adu)

    return Slice(index=image_slice.index,
                 units="electrons",
                 pixels=transform_adu_to_electron(image_slice.pixels))
