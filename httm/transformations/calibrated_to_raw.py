"""
Transformation functions for processing a :py:class:`~httm.data_structures.RAWConverter` so that it is suitable
for writing to a raw FITS file.
"""

import numpy

from constants import FPE_MAX_ADU
from ..data_structures import Slice


def add_start_of_line_ringing_to_slice(start_of_line_ringing, image_slice):
    # type: (numpy.ndarray, Slice) -> Slice
    """
    TODO.

    :param start_of_line_ringing:
    :type start_of_line_ringing: :py:class:`numpy.ndarray`
    :param image_slice:
    :type image_slice: Slice
    :rtype: Slice
    """
    pass


def add_pattern_noise_to_slice(pattern_noise, image_slice):
    # type: (numpy.ndarray, Slice) -> Slice
    """
    TODO.

    :param pattern_noise:
    :type pattern_noise: :py:class:`numpy.ndarray`
    :param image_slice:
    :type image_slice: Slice
    :rtype: Slice
    """
    pass


def introduce_smear_rows_to_slice(smear_ratio, image_slice):
    # type: (float, Slice) -> Slice
    """
    TODO.

    :param smear_ratio:
    :type smear_ratio: float
    :param image_slice:
    :type image_slice: Slice
    :rtype: Slice
    """
    # TODO crash if smear rows are not zero
    return image_slice


def add_shot_noise(image_slice):
    # type: (Slice) -> Slice
    """
    TODO. Currently done by SPyFFI.

    :param image_slice:
    :type image_slice: Slice
    :rtype: Slice
    """
    return image_slice


def simulate_blooming_on_slice(full_well, nreads, image_slice):
    """
    TODO. Currently done by SPyFFI

    :param image_slice:
    :param full_well:
    :param nreads:
    :type nreads: int
    :rtype: Slice
    """
    return image_slice


def add_readout_noise_to_slice(readout_noise, nreads, image_slice):
    """
    TODO. Currently done by SPyFFI.

    Adds a Gaussian random _readout_ noise to every pixel.
    The average value :math:`\\mu` of the noise is `0`.
    The variance :math:`\\sigma^2` is :math:`\\mathtt{readout\_noise}^2 \times \\mathtt{nreads}`

    :param image_slice:
    :type image_slice: :py:class:`~httm.data_structures.Slice`
    :param readout_noise:
    :type readout_noise: float
    :param nreads:
    :type nreads: int
    :rtype: Slice
    """
    from numpy.random import normal
    # noinspection PyProtectedMember
    return image_slice._replace(
        pixels=image_slice.pixels + normal(loc=0.0, scale=readout_noise * numpy.sqrt(nreads),
                                           size=image_slice.pixels.size))


# TODO: make this work on slices
def simulate_undershoot(row, undershoot):
    """
    When you have a bright pixel, the pixel to the right of it will appear dimmer.  This is _undershoot_.

    This function simulates undershoot for a slice.

    It convolves the kernel :math:`\\langle 1, -\\mathtt{undershoot}  \\rangle` with each input row,
    yielding an output row of the same length. The convolution is non-cyclic: the input row is implicitly
    padded with zero at the start to make this true.

    :param row: Full slice image row including all pixels dark and illuminated. Units: electrons
    :type row: :py:class:`numpy.ndarray`
    :param undershoot: Undershoot parameter from parameter structure, typically `~0.001`, dimensionless
    :type undershoot: float
    :rtype: :py:class:`numpy.ndarray`
    """
    kernel = numpy.array([1.0, -undershoot])
    return numpy.convolve(row, kernel, mode='same')


def convert_slice_electrons_to_adu(compression, number_of_exposures, video_scale, baseline_adu, image_slice):
    # type: (float, int, float, float, Slice) -> Slice
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

    return Slice(index=image_slice.index,
                 units="ADU",
                 pixels=transform_electron_to_adu(image_slice.pixels))


# noinspection PyProtectedMember
def convert_electrons_to_adu(calibrated_transformation):
    # type: (CalibratedConverter) -> CalibratedConverter
    """
    Converts a :py:class:`~httm.data_structures.CalibratedConverter` from having electrons
    to *Analogue to Digital Converter Units* (ADU).

    :param calibrated_transformation: Should have electrons for units
    :type calibrated_transformation: :py:class:`~httm.data_structures.CalibratedConverter`
    :rtype: :py:class:`~httm.data_structures.CalibratedConverter`
    """
    video_scales = calibrated_transformation.parameters.video_scales
    image_slices = calibrated_transformation.slices
    number_of_exposures = calibrated_transformation.fits_metadata.header['NREADS']
    compression = calibrated_transformation.parameters.compression
    baseline_adu = calibrated_transformation.parameters.baseline_adu
    assert len(video_scales) == len(image_slices), "Video scales do not match image slices"
    return calibrated_transformation._replace(
        slices=tuple(
            convert_slice_electrons_to_adu(compression, number_of_exposures, video_scale, image_slice, baseline_adu)
            for (video_scale, image_slice) in zip(video_scales, image_slices)))
