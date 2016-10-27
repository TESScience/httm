import numpy as np

def simulate_undershoot( row, undershoot ):
    """
    Simulate undershoot for one row.

    :param row: Full slice image row including all pixels dark and illuminated. Units: electrons
    :type row: :py:class:`numpy.ndarray`
    :param undershoot: Undershoot parameter from parameter structure, typically ~0.001, dimensionless
    :type undershoot: float
    :rtype: :py:class:`numpy.ndarray`
    """
    kernel = np.array([1.0,-undershoot])
    return np.convolve(row,kernel,mode='same')

def remove_undershoot( row, undershoot ):
    """
    Remove undershoot from one row.

    :param row: Full slice image row including all pixels dark and illuminated. Units: electrons
    :type row: :py:class:`numpy.ndarray`
    :param undershoot: Undershoot parameter from parameter structure, typically ~0.001, dimensionless
    :type undershoot: float
    :rtype: :py:class:`numpy.ndarray`
    """
    kernel = np.array([1.0,undershoot])
    return np.convolve(row,kernel,mode='same')
