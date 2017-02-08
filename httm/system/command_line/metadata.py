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
``httm.system.command_line.metadata``
=================================

This module contains metadata related to command line options.

  - ``command_line_options`` is metadata describing various command line options used by scripts.
"""
from collections import OrderedDict

command_line_options = OrderedDict([
    ('version', {
        'documentation': 'Print the version information.',
    }),
    ('config', {
        'type': 'str',
        'documentation': 'Set an optional configuration file.'
    }),
    ('help', {
        'documentation': 'Print the help message for this command line tool.'
    })
])
