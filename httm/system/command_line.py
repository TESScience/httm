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
``httm.system.command_line``
============================

This module contains utilities for parsing settings, such as parameter and flags, from the command line.
"""


# TODO: Documentation
def add_arguments_from_settings(argument_parser, setting_dictionary):
    for key in setting_dictionary:
        command_line_argument = '--' + key.replace('_', '-')  # type: str
        default = setting_dictionary[key]['default']
        argument_type = type(default)
        documentation_no_defaults = setting_dictionary[key]['documentation'] \
            .replace('`', '') \
            .replace('*', '')  # type: str
        if default is True or default is False:
            negative_command_line_argument = '--no-' + key.replace('_', '-')
            argument_parser.add_argument(
                negative_command_line_argument,
                default=None,
                dest=key,
                action='store_false')
            argument_parser.add_argument(
                command_line_argument,
                default=None,
                dest=key,
                action='store_true',
                help='{}. Default: Set to {}'.format(
                    documentation_no_defaults.rstrip('.'), str(default).upper()))
        elif hasattr(default, '__iter__') and not isinstance(default, str):
            argument_parser.add_argument(
                command_line_argument,
                default=None,
                dest=key,
                action='store',
                nargs='+',
                type=type(default[0]),
                help='{}. Default: {}'.format(documentation_no_defaults.rstrip('.'), default))
        else:
            argument_parser.add_argument(
                command_line_argument,
                dest=key,
                action='store',
                type=argument_type,
                default=None,
                help='{}. Default: {}'.format(documentation_no_defaults.rstrip('.'), default))
