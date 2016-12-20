"""
``httm.system.command_line``
============================

This module contains utilities for parsing settings, such as parameter and flags, from the command line.
"""
import re


def tidy_default(default_argument):
    if isinstance(default_argument, str):
        pattern_match = re.match(r'^:httm:(.*)', default_argument)
        if pattern_match:
            return 'built-in ' + pattern_match.group(1)
    else:
        return default_argument


# TODO: Documentation
def add_arguments_from_settings(argument_parser, setting_dictionary):
    for key in setting_dictionary:
        command_line_argument = '--' + key.replace('_', '-')  # type: str
        default = setting_dictionary[key]['default']
        argument_type = type(default)
        documentation_no_defaults = setting_dictionary[key]['documentation'] \
            .replace('`', '') \
            .replace('*', '')  # type: str
        if default is False:
            argument_parser.add_argument(
                command_line_argument,
                action='store_true',
                help=('{}'.format(documentation_no_defaults.rstrip('.') + ". Sets flag to True")))
        elif default is True:
            argument_parser.add_argument(
                '--no-' + key.replace('_', '-'),
                action='store_false',
                help=('{}'.format(documentation_no_defaults.rstrip('.') + ". Sets flag to False")))
        elif hasattr(default, '__iter__') and not isinstance(default, str):
            argument_parser.add_argument(
                command_line_argument,
                dest=key,
                action='store',
                nargs='+',
                type=type(default[0]),
                help=('{}. Default: {}'.format(documentation_no_defaults.rstrip('.'), default)))
        else:
            argument_parser.add_argument(
                command_line_argument,
                dest=key,
                action='store',
                type=argument_type,
                default=tidy_default(default),
                help=('{}. Default: {}'.format(documentation_no_defaults.rstrip('.'), default)))
