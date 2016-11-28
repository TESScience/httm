"""
``httm``
========

This module contains top level transformations for converting electron flux
to raw TESS full frame FITS images and raw to calibrated TESS full frame FITS images.
"""
from collections import OrderedDict
from functools import reduce

from .fits_utilities.electron_flux_fits import electron_flux_converter_from_hdulist, \
    electron_flux_converter_to_simulated_raw_hdulist, electron_flux_converter_from_fits, \
    write_electron_flux_converter_to_simulated_raw_fits
from .fits_utilities.raw_fits import raw_converter_from_hdulist, raw_converter_to_calibrated_hdulist, \
    raw_converter_from_fits, write_raw_converter_to_calibrated_fits
from .transformations.electron_flux_converters_to_raw import electron_flux_transformation_default_settings, \
    electron_flux_transformation_functions
from .transformations.raw_converters_to_calibrated import raw_transformation_default_settings, \
    raw_transformation_functions


def derive_transformation_function_list(transformation_settings, default_settings, transformation_functions):
    # type: (OrderedDict, OrderedDict) -> tuple
    if isinstance(transformation_settings, dict):
        for key, value in transformation_settings.items():
            if key not in default_settings:
                raise ValueError("Unknown raw transformation: {key}".format(key=key))
            if not isinstance(value, bool):
                raise ValueError("Value for raw transformation {key} "
                                 "must be True or False, was {value}".format(key=key, value=value))
    return tuple(transformation_functions[k]
                 for k in default_settings.keys() if
                 k not in transformation_settings and default_settings[k] or transformation_settings.get(k, False))


# TODO: Documentation
def transform_raw_converter(single_ccd_raw_converter, transformation_settings=raw_transformation_default_settings):
    """

    :param single_ccd_raw_converter:
    :param transformation_settings:
    :return:
    """
    return reduce(lambda converter, transformation_function: transformation_function(converter),
                  derive_transformation_function_list(transformation_settings, raw_transformation_default_settings,
                                                      raw_transformation_functions),
                  initial=single_ccd_raw_converter)


# TODO: Documentation
# TODO: Test
def raw_hdulist_to_calibrated(hdulist, origin_file_name=None, flags=None, parameters=None,
                              transformation_settings=raw_transformation_default_settings):
    """
    Convert an :py:class:`astropy.io.fits.HDUList` containing raw FITS image data
    (in *Analogue to Digital Converter Units*) to an :py:class:`astropy.io.fits.HDUList` containing calibrated data).

    :param hdulist:
    :param origin_file_name:
    :param flags:
    :param parameters:
    :param transformation_settings:
    """
    single_ccd_raw_converter = raw_converter_from_hdulist(hdulist, origin_file_name=origin_file_name, flags=flags,
                                                          parameters=parameters)
    return raw_converter_to_calibrated_hdulist(
        transform_raw_converter(single_ccd_raw_converter, transformation_settings=transformation_settings))


# TODO: Documentation
# TODO: Test
def raw_fits_to_calibrated(fits_input_file, fits_output_file, flags=None, parameters=None,
                           transformation_settings=raw_transformation_default_settings):
    """
    TODO


    :param fits_input_file:
    :param fits_output_file:
    :param flags:
    :param parameters:
    :param transformation_settings:
    """
    single_ccd_raw_converter = raw_converter_from_fits(fits_input_file, flags=flags, parameters=parameters)
    write_raw_converter_to_calibrated_fits(
        transform_raw_converter(single_ccd_raw_converter, transformation_settings=transformation_settings),
        fits_output_file)


# TODO: Documentation
def transform_electron_flux_converter(single_ccd_electron_flux_converter,
                                      transformation_settings=electron_flux_transformation_default_settings):
    """

    :param single_ccd_electron_flux_converter:
    :param transformation_settings:
    :return:
    """
    return reduce(lambda converter, transformation_function: transformation_function(converter),
                  derive_transformation_function_list(transformation_settings,
                                                      electron_flux_transformation_default_settings,
                                                      electron_flux_transformation_functions),
                  initial=single_ccd_electron_flux_converter)


# TODO: Documentation
# TODO: Test
def electron_flux_hdulist_to_simulated_raw(hdulist, origin_file_name=None, flags=None, parameters=None,
                                           transformation_settings=electron_flux_transformation_default_settings):
    """
    TODO

    :param hdulist:
    :param origin_file_name:
    :param flags:
    :param parameters:
    :param transformation_settings:
    """
    single_ccd_electron_flux_converter = electron_flux_converter_from_hdulist(hdulist,
                                                                              origin_file_name=origin_file_name,
                                                                              flags=flags,
                                                                              parameters=parameters)
    return electron_flux_converter_to_simulated_raw_hdulist(
        transform_electron_flux_converter(single_ccd_electron_flux_converter,
                                          transformation_settings=transformation_settings))


# TODO: Documentation
# TODO: Test
def electron_flux_fits_to_raw(fits_input_file, fits_output_file, flags=None, parameters=None,
                              transformation_settings=electron_flux_transformation_default_settings):
    """
    TODO

    :param fits_input_file:
    :param fits_output_file:
    :param flags:
    :param parameters:
    :param transformation_settings:
    """
    single_ccd_electron_flux_converter = electron_flux_converter_from_fits(fits_input_file, flags=flags,
                                                                           parameters=parameters)
    write_electron_flux_converter_to_simulated_raw_fits(
        transform_electron_flux_converter(single_ccd_electron_flux_converter,
                                          transformation_settings=transformation_settings),
        fits_output_file)


# TODO: Documentation
# TODO: Test
def simulate_electronic_effects_on_hdulist(
        hdulist,
        origin_file_name=None,
        electron_flux_flags=None,
        electron_flux_parameters=None,
        electron_flux_transformation_settings=electron_flux_transformation_default_settings,
        raw_flags=None,
        raw_parameters=None,
        raw_transformation_settings=raw_transformation_default_settings,
):
    """

    :param hdulist:
    :param origin_file_name:
    :param electron_flux_flags:
    :param electron_flux_parameters:
    :param electron_flux_transformation_settings:
    :param raw_flags:
    :param raw_parameters:
    :param raw_transformation_settings:
    :rtype: :py:class:`astropy.io.fits.HDUList`
    """
    simulated_raw_hdulist = electron_flux_hdulist_to_simulated_raw(
        hdulist,
        origin_file_name=origin_file_name,
        flags=electron_flux_flags,
        parameters=electron_flux_parameters,
        transformation_settings=electron_flux_transformation_settings,
    )
    return raw_hdulist_to_calibrated(
        simulated_raw_hdulist,
        origin_file_name=origin_file_name,
        flags=raw_flags,
        parameters=raw_parameters,
        transformation_settings=raw_transformation_settings,
    )


# TODO: Document me
# TODO: Test me
def simulate_electronic_effects_on_fits(
        fits_input_file,
        fits_output_file,
        electron_flux_flags=None,
        electron_flux_parameters=None,
        electron_flux_transformation_settings=electron_flux_transformation_default_settings,
        raw_flags=None,
        raw_parameters=None,
        raw_transformation_settings=raw_transformation_default_settings,
):
    """

    :param fits_input_file:
    :param fits_output_file:
    :param electron_flux_flags:
    :param electron_flux_parameters:
    :param electron_flux_transformation_settings:
    :param raw_flags:
    :param raw_parameters:
    :param raw_transformation_settings:
    """
    single_ccd_electron_flux_converter = electron_flux_converter_from_fits(
        fits_input_file,
        flags=electron_flux_flags,
        parameters=electron_flux_parameters,
    )
    simulated_raw_hdulist = electron_flux_converter_to_simulated_raw_hdulist(
        transform_electron_flux_converter(single_ccd_electron_flux_converter,
                                          transformation_settings=electron_flux_transformation_settings))
    single_ccd_raw_converter = raw_converter_from_hdulist(
        simulated_raw_hdulist,
        origin_file_name=single_ccd_electron_flux_converter.fits_metadata.origin_file_name,
        flags=raw_flags,
        parameters=raw_parameters,
    )
    write_raw_converter_to_calibrated_fits(
        transform_raw_converter(single_ccd_raw_converter, transformation_settings=raw_transformation_settings),
        fits_output_file)
