# HTTM: A transformation library for RAW and Electron Flux TESS Images
# Copyright (C) 2016, 2017 John Doty and Matthew Wampler-Doty of Noqsi Aerospace, Ltd.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""
``httm.transformations.common``
===============================

Common utilities used in the transformation of :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter`
and :py:class:`~httm.data_structures.electron_flux_converter.SingleCCDElectronFluxConverter` objects.
"""

import logging

logger = logging.getLogger(__name__)


def derive_transformation_function_list(transformation_settings,
                                        default_settings,
                                        transformation_functions):
    """
    Internal helper function for deriving a tuple of transformation functions from a settings object.

    Settings objects are ``namedtuple`` objects or a ``namespace`` derived from
    :py:method:`argparse.ArgumentParser.parse_args`

    Keys specified in a ``default_dictionary`` are assumed to be attributes in the ``transformation_settings`` object.

    Transformations are sensitive to order, which is why the ``default_dictionary`` is an
    :py:class:`collections.OrderedDict` rather than a simple ``dict`` and hence dictates the order of transformations.

    If an attribute is missing or is set to ``None``, a default specified in the ``default_dictionary`` is used.

    Functions are specified in a dictionary ``transformation_functions``, specified by the same keys used in the
    ``default_settings`` dictionary.

    :param transformation_settings: An object containing explicit settings for which functions to run.
    :type transformation_settings: object
    :param default_settings: A dictionary whose keys are intended to be read as attributes of the \
    ``transformation_settings`` object, with default settings to fall back to.
    :type default_settings: :py:class:`collections.OrderedDict`
    :param transformation_functions: A dictionary of transformation functions
    :type transformation_functions: dict
    :rtype: A tuple of functions
    """

    def check_if_specified_or_default(key):
        if hasattr(transformation_settings, key):
            value = getattr(transformation_settings, key)
            if value is not None:
                if value is True or value is False:
                    logger.info('Key "{key}" was set to {value}'.format(
                        key=key,
                        value=value))
                    return value
                else:
                    raise Exception("Value must be either True or False, was: {}".format(value))
        logger.info(
            'Key "{key}" using default: {value}'.format(
                key=key,
                value=default_settings[key]))
        return default_settings[key]

    return tuple(transformation_functions[k]
                 for k in default_settings.keys() if
                 check_if_specified_or_default(k))
