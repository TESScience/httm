"""
``httm``
========

This module contains top level transformations for converting electron flux
to raw TESS full frame FITS images and raw to calibrated TESS full frame FITS images.
"""

import logging

from .fits_utilities.electron_flux_fits import electron_flux_converter_from_hdulist, \
    electron_flux_converter_to_simulated_raw_hdulist, electron_flux_converter_from_fits, \
    write_electron_flux_converter_to_simulated_raw_fits
from .fits_utilities.raw_fits import raw_converter_from_hdulist, raw_converter_to_calibrated_hdulist, \
    raw_converter_from_fits, write_raw_converter_to_calibrated_fits
from .transformations.electron_flux_converters_to_raw import electron_flux_transformation_default_settings, \
    electron_flux_transformation_functions
from .transformations.raw_converters_to_calibrated import raw_transformation_default_settings, \
    raw_transformation_functions

logger = logging.getLogger(__name__)


# TODO: Documentation
def derive_transformation_function_list(transformation_settings, default_settings, transformation_functions):
    """

    :param transformation_settings:
    :type transformation_settings: object
    :param default_settings:
    :type default_settings: dictionary
    :param transformation_functions:
    :type transformation_functions: dictionary
    :rtype:
    """

    def check_if_specified_or_default(key):
        if hasattr(transformation_settings, key):
            value = getattr(transformation_settings, key)
            if value is not None:
                if value is True or value is False:
                    logger.info('Key "{key}" was set to {value}'.format(key=key, value=value))
                    return value
                else:
                    raise Exception("Value must be either True or False, was: {}".format(value))
        logger.info('Key "{key}" using default: {value}'.format(key=key, value=default_settings[key]))
        return default_settings[key]

    return tuple(transformation_functions[k] for k in default_settings.keys() if check_if_specified_or_default(k))


# TODO: Documentation
def transform_raw_converter(single_ccd_raw_converter, transformation_settings=None):
    """

    :param single_ccd_raw_converter:
    :param transformation_settings:
    :return:
    """
    from functools import reduce
    return reduce(lambda converter, transformation_function: transformation_function(converter),
                  derive_transformation_function_list(transformation_settings,
                                                      raw_transformation_default_settings,
                                                      raw_transformation_functions),
                  single_ccd_raw_converter)


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
    single_ccd_raw_converter = raw_converter_from_hdulist(hdulist, origin_file_name=origin_file_name,
                                                          flag_overrides=flags,
                                                          parameter_overrides=parameters)
    return raw_converter_to_calibrated_hdulist(
        transform_raw_converter(single_ccd_raw_converter, transformation_settings=transformation_settings))


# TODO: Documentation
def raw_fits_to_calibrated(fits_input_file, fits_output_file, flag_overrides=None, parameter_overrides=None,
                           transformation_settings=raw_transformation_default_settings):
    """
    TODO


    :param fits_input_file:
    :param fits_output_file:
    :param flag_overrides:
    :param parameter_overrides:
    :param transformation_settings:
    """
    single_ccd_raw_converter = raw_converter_from_fits(fits_input_file, flag_overrides=flag_overrides,
                                                       parameter_overrides=parameter_overrides)
    write_raw_converter_to_calibrated_fits(
        transform_raw_converter(single_ccd_raw_converter, transformation_settings=transformation_settings),
        fits_output_file)


# TODO: Documentation
def transform_electron_flux_converter(single_ccd_electron_flux_converter,
                                      transformation_settings=None):
    """

    :param single_ccd_electron_flux_converter:
    :param transformation_settings:
    :return:
    """
    from functools import reduce
    import numpy.random
    numpy.random.seed(single_ccd_electron_flux_converter.parameters.random_seed)
    return reduce(lambda converter, transformation_function: transformation_function(converter),
                  derive_transformation_function_list(transformation_settings,
                                                      electron_flux_transformation_default_settings,
                                                      electron_flux_transformation_functions),
                  single_ccd_electron_flux_converter)


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
                                                                              flag_overrides=flags,
                                                                              parameter_overrides=parameters)
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
    single_ccd_electron_flux_converter = electron_flux_converter_from_fits(fits_input_file, flag_overrides=flags,
                                                                           parameter_overrides=parameters)
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
        flag_overrides=electron_flux_flags,
        parameter_overrides=electron_flux_parameters,
    )
    simulated_raw_hdulist = electron_flux_converter_to_simulated_raw_hdulist(
        transform_electron_flux_converter(single_ccd_electron_flux_converter,
                                          transformation_settings=electron_flux_transformation_settings))
    single_ccd_raw_converter = raw_converter_from_hdulist(
        simulated_raw_hdulist,
        origin_file_name=single_ccd_electron_flux_converter.conversion_metadata.origin_file_name,
        flag_overrides=raw_flags,
        parameter_overrides=raw_parameters,
    )
    write_raw_converter_to_calibrated_fits(
        transform_raw_converter(single_ccd_raw_converter, transformation_settings=raw_transformation_settings),
        fits_output_file)
