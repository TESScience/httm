"""
``httm``
========

This module contains top level transformations for converting calibrated
or raw TESS full frame FITS images between one another.
"""

from fits_utilities.raw_fits import raw_converter_from_HDUList, raw_converter_to_HDUList


# TODO: Write me
def raw_hdulist_to_calibrated(hdulist, origin_file_name=None, flags=None, parameters=None):
    """
    TODO: Document me

    :param hdulist:
    :param origin_file_name:
    :param flags:
    :param parameters:
    """
    # TODO: Run transformations
    return raw_converter_to_HDUList(
        raw_converter_from_HDUList(hdulist, origin_file_name=origin_file_name, flags=flags, parameters=parameters))


# TODO: Write me
def raw_fits_to_calibrated(fits_input_file, fits_output_file):
    """
    TODO

    :param fits_input_file:
    :param fits_output_file:
    """
    pass


# TODO: Write me
def calibrated_hdulist_to_raw(hdulist):
    """
    TODO

    :param hdulist:
    """
    pass


# TODO: Write me
def calibrated_fits_to_raw(fits_input_file, fits_output_file):
    """
    TODO

    :param fits_input_file:
    :param fits_output_file:
    """
    pass


# TODO: Write me
def simulate_electronic_effects_on_hdulist(hdulist):
    """
    TODO

    :param hdulist:
    """
    pass


# TODO: Write me
def simulate_electronic_effects_on_fits(fits_input_file, fits_output_file):
    """
    TODO

    :param fits_input_file:
    :param fits_output_file:
    """
    pass
