"""
``httm``
========

This module contains top level transformations for converting electron flux
to raw TESS full frame FITS images and raw to calibrated TESS full frame FITS images.
"""

from .fits_utilities.raw_fits import raw_converter_from_HDUList, raw_converter_to_calibrated_HDUList
from .transformations.raw_converters_to_calibrated import raw_transformation_defaults


# TODO: Write me
def raw_hdulist_to_calibrated(hdulist, origin_file_name=None, flags=None, parameters=None,
                              transformations=raw_transformation_defaults):
    """
    TODO: Document me

    :param hdulist:
    :param origin_file_name:
    :param flags:
    :param parameters:
    :param transformations:
    """
    if isinstance(transformations, dict):
        for key, value in transformations.items():
            if key not in transformations:
                raise ValueError("Unknown raw transformation: {key}".format(key=key))
            if not isinstance(value, bool):
                raise ValueError("Value for raw transformation {key} "
                                 "must be True or False, was {value}".format(key=key, value=value))

    # TODO: Run transformations
    return raw_converter_to_calibrated_HDUList(
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
def electron_flux_hdulist_to_raw(hdulist):
    """
    TODO

    :param hdulist:
    """
    pass


# TODO: Write me
def electron_flux_fits_to_raw(fits_input_file, fits_output_file):
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
