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
``httm.data_structures.documentation``
========================

This module contains facilities for documenting parameters from dictionary descriptions.
"""


def document_parameters(parameter_dictionary):
    """
    Construct a documentation string for dictionary of parameters

    :param parameter_dictionary: An ordered dictionary of parameters,\
    where each entry contains a ``type``, ``documentation`` string, and ``default`` value.
    :type parameter_dictionary: :py:class:`collections.OrderedDict`
    :rtype: str
    """
    return '\n'.join([":param {parameter}: {documentation}. Default: ``{default}``\n"
                      ":type {parameter}: {type}"
                     .format(parameter=parameter,
                             documentation=data['documentation'].rstrip(". "),
                             default=data['default'],
                             type=data['type'])
                      for parameter, data in parameter_dictionary.items()])
