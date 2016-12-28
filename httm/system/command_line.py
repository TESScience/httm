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
