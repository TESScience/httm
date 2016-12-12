"""
``httm.fits_utilities.header_settings``
=======================================

This module contains functions for parsing settings, such as parameter or flags,
from a FITS file header.
"""
import logging

logger = logging.getLogger(__name__)


# TODO: Fall back to alternate FITS headers
def get_header_setting(key_name, setting_dictionary, fits_header, override_value=None):
    assert key_name in setting_dictionary, "Unknown key: {}".format(key_name)

    for forbidden_fits_keyword in setting_dictionary[key_name].get('forbidden_fits_keyword', []):
        if forbidden_fits_keyword in fits_header:
            logger.warning("Forbidden FITS keyword present: {}".format(forbidden_fits_keyword))

    if override_value is not None:
        return override_value

    fits_keyword = setting_dictionary[key_name]['standard_fits_keyword']

    default_value = setting_dictionary[key_name]['default']

    if isinstance(fits_keyword, str):
        if setting_dictionary[key_name]['required_keyword'] and fits_keyword not in fits_header:
            logger.warning("Required FITS keyword not present: {}".format(fits_keyword))
        if fits_keyword in fits_header:
            assert isinstance(fits_header[fits_keyword], type(default_value))
            return fits_header[fits_keyword]
        else:
            return default_value

    elif hasattr(fits_keyword, '__iter__'):
        assert len(fits_keyword) is len(default_value)
        for unsorted_fits_keyword, sorted_fits_keyword in zip(fits_keyword, sorted(fits_keyword)):
            assert unsorted_fits_keyword is sorted_fits_keyword, \
                "FITS keyword is out of order {}".format(unsorted_fits_keyword)

        return tuple(fits_header[subkeyword] if subkeyword in fits_header else default_subvalue
                     for subkeyword, default_subvalue in zip(fits_keyword, default_value))

    else:
        raise Exception("Cannot handle fits keyword format: {}".format(fits_keyword))
