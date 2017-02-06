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
``httm.system.config_file``
===========================

This module contains utilities for parsing config files into data structures suitable for constructing
parameter or flag data structures.
"""

import json
import os
import re
import sys
from collections import namedtuple, Iterable

import toml


def convert_to_type(input_data, value_type):
    """
    Convert a string value into a specified type

    :param input_data: Input to parse
    :param value_type: Type of the result
    :type value_type: type
    :return: The parsed string
    """
    if value_type is str:
        return str(input_data)
    if value_type is float:
        return float(input_data)
    if value_type is int:
        return int(input_data)
    if value_type is bool:
        return bool(json.loads(input_data.lower()))
    if value_type is tuple:
        if isinstance(input_data, str):
            return tuple(json.loads(input_data))
        if isinstance(input_data, Iterable):
            return tuple(json.loads(datum) for datum in input_data)
    raise Exception("Unknown type: {}".format(value_type))


def flatten_dictionary(dictionary):
    """
    Recursively flattens a dictionary containing other dictionaries into a single dictionary

    :param dictionary: Dictionary to flatten
    :type dictionary: dict
    :rtype dict
    """
    result = {}
    for k in dictionary:
        value = dictionary[k]
        if isinstance(value, dict):
            result.update(flatten_dictionary(value))
        elif value is not None:
            result[k.replace("-", "_")] = value
    return result


def parse_dict(dictionary, reference_dictionaries, convert=False, override=None):
    """
    Parse a dictionary into a ``namedtuple`` with specified attributes given by the reference dictionaries

    Recursively flattens a dictionary prior to parsing

    :param dictionary: A dictionary to parse
    :type dictionary: dict
    :param reference_dictionaries: A list of reference dictionaries
    :type reference_dictionaries: list
    :param convert: Flag which specifies whether to convert dictionary values to types specified by the default values \
    in the reference dictionaries
    :type convert: bool
    :param override: An object with attributes that override values set in the dictionary to be parsed
    :type override: object
    :rtype: namedtuple
    """
    reference = {}
    for d in reference_dictionaries:
        reference.update(d)
    flat_dictionary = flatten_dictionary(dictionary)
    for raw_k in flat_dictionary:
        k = raw_k.replace("-", "_").lower()
        if k not in reference:
            raise Exception('Unknown key: "{key}"\n'
                            'Available keys (with defaults): {keys}'.format(key=k,
                                                                            keys=", ".join(
                                                                                '{key}={default}'.format(
                                                                                    key=key,
                                                                                    default=reference[key]['default'])
                                                                                for key in
                                                                                sorted(reference.keys()))))
        else:
            if convert:
                if reference[k]['default'] is None:
                    flat_dictionary[k] = json.loads(flat_dictionary[k])
                else:
                    flat_dictionary[k] = convert_to_type(flat_dictionary[k], type(reference[k]['default']))
            # Use the override value if it is set
            if hasattr(override, k) and getattr(override, k) is not None:
                flat_dictionary[k] = getattr(override, k)
            # Check the type in the dictionary, but be very liberal
            # Note: Unicode is deprecated in Python 3, but strings are sometimes parsed as unicode in Python 2.7
            # noinspection PyUnresolvedReferences
            if not isinstance(flat_dictionary[k], type(reference[k]['default'])) and \
                    not reference[k]['default'] is None and \
                    not (sys.version_info <= (3, 0) and
                         isinstance(flat_dictionary[k], unicode) and
                         isinstance(reference[k]['default'], str)) and \
                    not (isinstance(flat_dictionary[k], list) and isinstance(reference[k]['default'], tuple)) and \
                    not (isinstance(flat_dictionary[k], float) and isinstance(reference[k]['default'], int)) and \
                    not (isinstance(flat_dictionary[k], int) and isinstance(reference[k]['default'], float)):
                raise Exception(
                    'Expected key "{key}" with value {value} to have type {expected_type}, '
                    'but had type {actual_type}'.format(
                        key=k,
                        value=flat_dictionary[k],
                        expected_type=type(reference[k]['default']),
                        actual_type=type(flat_dictionary[k])))
    return namedtuple('ParametersAndFlags', flat_dictionary.keys())(**flat_dictionary)


def remove_comments(line, comment_separator='#'):
    """
    Remove comments from a line

    :param line: Line to remove comments from
    :type line: str
    :param comment_separator: Delimiter for comments
    :type comment_separator: str
    :rtype: str
    """
    return line.split(comment_separator)[0].strip()


def format_lists(line):
    """
    Format lists contained in a string to not have whitespaces

    :param line: Line to format
    :type line: str
    :rtype: str
    """
    comma = re.compile(r',\W*')
    left_bracket = re.compile(r'\[\W*')
    right_bracket = re.compile(r'\W*]')
    return re.sub(right_bracket, ']', re.sub(left_bracket, '[', re.sub(comma, ',', line)))


def parse_tsv_line(line, separator_regex):
    """
    Parse a TSV line into non-empty columns with whitespace stripped

    :param line: Line to parse
    :type line: str
    :param separator_regex: Compiled regex representing the column separators for a TSV
    :rtype: str
    """
    no_quotes = line.replace('"', '')
    stripped_comments = remove_comments(no_quotes, '#')
    clean_line = format_lists(stripped_comments)
    columns = re.sub(separator_regex, '\t', clean_line).split('\t')
    clean_columns = map(lambda x: x.strip(), columns)
    return filter(lambda x: x != '', clean_columns)


def parse_tsv(filename, reference_dictionaries, override=None):
    """
    Parses a TSV file into a namedtuple.

    Only uses the first two non-empty columns.

    Lines with zero or one columns are skipped.

    :param filename: File to parse
    :type filename: str
    :param reference_dictionaries: List of dictionaries to use when creating a namedtuple
    :type reference_dictionaries: list
    :param override: Object with attributes that override values set by the dictionary
    :type override: object
    :rtype: namedtuple
    """
    with open(filename, 'r') as f:
        value_dictionary = {}
        separator = re.compile(r'(\t[\t ]*|[ ][ ]+)')
        for l in f.readlines():
            try:
                key_value = tuple(parse_tsv_line(l, separator))
                if len(key_value) <= 1:
                    continue
                value_dictionary[key_value[0].strip()] = key_value[1].strip()
            except:
                raise RuntimeError("Could not parse TSV line: {}".format(l))
        return parse_dict(value_dictionary, reference_dictionaries,
                          convert=True,
                          override=override)


def parse_toml(filename, reference_dictionaries, override=None):
    """
    Parse a TOML file into a namedtuple

    :param filename: File to parse
    :type filename: str
    :param reference_dictionaries: List of dictionaries to use when creating a namedtuple
    :type reference_dictionaries: list
    :param override: Object with attributes that override values set by the dictionary
    :type override: object
    :rtype: namedtuple
    """
    return parse_dict(toml.load(filename), reference_dictionaries, override=override)


def parse_json(filename, reference_dictionaries, override=None):
    """
    Parse a JSON file into a namedtuple

    :param filename: File to parse
    :type filename: str
    :param reference_dictionaries: List of dictionaries to use when creating a namedtuple
    :type reference_dictionaries: list
    :param override: Object with attributes that override values set by the dictionary
    :type override: object
    :rtype: namedtuple
    """
    with open(filename, 'r') as f:
        return parse_dict(json.load(f), reference_dictionaries, override=override)


def parse_config(filename, reference_dictionaries, override=None):
    """
    Parse a file into a named tuple, based on suffix.

    Supported file types are: JSON, XML, TSV, YAML, and TOML.

    :param filename: File to parse
    :type filename: str
    :param reference_dictionaries: List of dictionaries to use when creating a namedtuple
    :type reference_dictionaries: list
    :param override: Object with attributes that override values set by the dictionary
    :type override: object
    :rtype: namedtuple
    """

    _, suffix = os.path.splitext(filename.lower())

    if suffix == '.tsv':
        return parse_tsv(filename, reference_dictionaries, override=override)
    if suffix == '.toml':
        return parse_toml(filename, reference_dictionaries, override=override)
    if suffix == '.json':
        return parse_json(filename, reference_dictionaries, override=override)

    raise Exception('Unsupported file format for {filename} (inferred suffix as "{suffix}")'.format(
        filename=filename,
        suffix=suffix,
    ))
