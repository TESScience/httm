"""
Transformation functions for processing a :py:class:`~httm.data_structures.RAWTransformation` so that it it suitable
for writing to a calibrated FITS file.
"""
import numpy


def remove_undershoot(row, undershoot):
    """
    Remove undershoot from one row.

    :param row: Full slice image row including all pixels dark and illuminated. Units: electrons
    :type row: :py:class:`numpy.ndarray`
    :param undershoot: Undershoot parameter from parameter structure, typically ~0.001, dimensionless
    :type undershoot: float
    :rtype: :py:class:`numpy.ndarray`
    """
    kernel = numpy.array([1.0, undershoot])
    return numpy.convolve(row, kernel, mode='same')
