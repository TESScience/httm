"""
``httm.fits_utilities.header_settings``
=======================================

This module contains functions for parsing settings, such as parameter or flags,
from a FITS file header.
"""

import logging

from astropy.io.fits import Header

logger = logging.getLogger(__name__)


# TODO: Documentation
def set_header_settings(settings, setting_dictionary, fits_header):
    updated_header = Header(fits_header, copy=True)
    for key_name in setting_dictionary:
        value = getattr(settings, key_name)
        fits_keyword = setting_dictionary[key_name]['standard_fits_keyword']
        fits_documentation = setting_dictionary[key_name]['short_documentation'] \
            if 'short_documentation' in setting_dictionary[key_name] \
            else setting_dictionary[key_name]['documentation']
        if isinstance(fits_keyword, str):  # if the fits_keyword is a string
            if fits_keyword in updated_header and updated_header[fits_keyword] != value:
                logger.warning(
                    'FITS keyword "{fits_keyword}" is set to value "{fits_value}", '
                    'overriding with value "{new_value}"'.format(
                        fits_keyword=fits_keyword,
                        fits_value=updated_header[fits_keyword],
                        new_value=value))
            updated_header[fits_keyword] = value, fits_documentation
        elif hasattr(fits_keyword, '__iter__'):  # if the fits_keyword is a list
            for k, slice_index, v in zip(fits_keyword, range(len(value)), value):
                if k in updated_header and updated_header[k] != v:
                    logger.warning(
                        'FITS keyword "{fits_keyword}" is set to value "{fits_value}", '
                        'overriding with value "{new_value}"'.format(
                            fits_keyword=k,
                            fits_value=updated_header[k],
                            new_value=v))
                updated_header[k] = v, "{documentation} Slice: {slice_index}".format(
                    documentation=fits_documentation,
                    slice_index=slice_index
                )
    return updated_header


# TODO: Documentation
def get_header_setting(key_name, setting_dictionary, fits_header, override_value=None):
    """

    :param key_name:
    :param setting_dictionary:
    :param fits_header:
    :param override_value:
    :return:
    """
    assert key_name in setting_dictionary, "Unknown key: {}".format(key_name)

    for forbidden_fits_keyword in setting_dictionary[key_name].get('forbidden_fits_keyword', []):
        if forbidden_fits_keyword in fits_header:
            logger.warning("Forbidden FITS keyword present: {}".format(forbidden_fits_keyword))

    if override_value is not None:
        return override_value

    fits_keyword = setting_dictionary[key_name]['standard_fits_keyword']

    default_value = setting_dictionary[key_name]['default']

    if isinstance(fits_keyword, str):  # if the fits_keyword is a string
        if setting_dictionary[key_name]['required_keyword'] and fits_keyword not in fits_header:
            logger.warning("Required FITS keyword not present: {}".format(fits_keyword))
        if fits_keyword in fits_header:
            assert isinstance(fits_header[fits_keyword], type(default_value))
            return fits_header[fits_keyword]
        else:
            assert 'alternate_fits_keywords' in setting_dictionary[key_name], \
                "No 'alternate_fits_keywords' for {}".format(key_name)
            for alternate_key in setting_dictionary[key_name]['alternate_fits_keywords']:
                if alternate_key in fits_header:
                    assert isinstance(fits_header[alternate_key], type(default_value))
                    logger.warning(
                        'Required FITS keyword "{}" falling back to "{}"'.format(fits_keyword, alternate_key))
                    return fits_header[alternate_key]
            return default_value

    elif hasattr(fits_keyword, '__iter__'):  # if the fits_keyword is a list
        assert len(fits_keyword) is len(default_value)
        for unsorted_fits_keyword, sorted_fits_keyword in zip(fits_keyword, sorted(fits_keyword)):
            assert unsorted_fits_keyword is sorted_fits_keyword, \
                "FITS keyword is out of order {}".format(unsorted_fits_keyword)

        return tuple(fits_header[subkeyword] if subkeyword in fits_header else default_subvalue
                     for subkeyword, default_subvalue in zip(fits_keyword, default_value))

    else:
        raise Exception("Cannot handle fits keyword (invalid format): {}".format(fits_keyword))
