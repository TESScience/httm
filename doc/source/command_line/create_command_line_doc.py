#!/usr/bin/env python2.7

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

from __future__ import print_function

import re
from importlib import import_module
from os import listdir
from os.path import isfile, join

from httm.data_structures.metadata import parameters, transformation_flags
from httm.transformations.metadata import electron_flux_transformations, raw_transformations
from httm.system.command_line.metadata import command_line_options

key_data = parameters.copy()
key_data.update(transformation_flags)
key_data.update(command_line_options)
key_data.update(electron_flux_transformations)
key_data.update(raw_transformations)


def format_usage(name_of_script, option_parser):
    usage = option_parser.format_usage()
    lines = usage.replace(__file__, name_of_script).split('\n')
    (first_line, second_line) = re.compile('\[-h\] ').split(lines[0])
    return ("```\n{}\n```".format(
        '\n'.join([first_line] + list('       ' + l.strip() for l in ['[-h] ' + second_line] + lines[1:]))))


def get_keys_from_usage(option_parser):
    matcher = re.compile('.*\[--(?:no-)?([\w\-]+)')
    matches = (matcher.match(l.strip()) for l in option_parser.format_usage().split(']'))
    options = ["help"] + [m.group(1) for m in matches if m is not None]
    visited = set()
    return [o.replace("-", "_") for o in options if o is not None and o not in visited and (visited.add(o) or True)]


def format_option(option_key):
    # type: (str) -> str
    if 'default' in key_data[option_key] and isinstance(key_data[option_key]['default'], bool):
        return "### `--{option}` / `--no-{option}`".format(option=option_key.replace("_", "-"))
    else:
        return "### `--{}`".format(option_key.replace("_", "-"))

if __name__ == "__main__":
    print("# Command Line Utilities")
    scripts = [f for f in listdir("scripts") if isfile(join("scripts", f)) and f != "__init__.py" and f.endswith('.py')]
    for script in scripts:
        # Print script name
        script_name = script.split('.')[0]
        print("## `{}`\n".format(script_name))

        # Get the command line argument parser from the script
        argument_parser = import_module("scripts.{}".format(script_name)).argument_parser

        # Print the description of the command line utility
        print(argument_parser.description + "\n")

        # Print the usage
        print(format_usage(script_name, argument_parser) + "\n")

        # Print Help
        for key in get_keys_from_usage(argument_parser):
            print(format_option(key) + "\n")
            print(key_data[key]['documentation'] + "\n")
