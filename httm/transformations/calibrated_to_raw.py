"""
Transformation functions for processing a :py:class:`~httm.data_structures.RAWTransformation` so that it it suitable
for writing to a raw FITS file.
"""

import numpy

def add_smear( data, smear_ratio, smear_row_count ):
    """
    STUB.

    :param data:
    :param smear_ratio:
    :param smear_row_count:
    :return:
    """

    return data

def add_shot_noise( data ):
    """
    STUB. Currently done by SPyFFI.

    :param data:
    :return:
    """

    return data

def do_blooming( data, full_well, nreads):
    """
    STUB. Currently done by SPyFFI

    :param data:
    :param full_well:
    :param nreads:
    :return:
    """

    return data

def add_readout_noise( data, readout_noise, nreads ):
    """
    STUB. Currently done by SPyFFI.

    :param data:
    :param readout_noise:
    :return:
    """

    return data

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
