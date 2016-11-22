#!/usr/bin/env python
from __future__ import print_function

import importlib
import re
import sys


def check_if_python_object_exists(full_python_object_name):
    # type: (str) -> NoneType
    """
    Check if a specified python object name exists.  Throw an exception if it does not.

    :type full_python_object_name: str
    :param full_python_object_name: A String containing the python docstring to look for
    """
    assert re.compile("^[a-zA-Z_][a-zA-Z0-9_.]*[a-zA-Z0-9_]").match(full_python_object_name) is not None, \
        "Invalid python object name {}".format(full_python_object_name)
    python_object_part_names = full_python_object_name.split(".")  # type: tuple
    if len(python_object_part_names) == 1:
        importlib.import_module(python_object_part_names[0])
    else:
        module_name = ".".join(python_object_part_names[:-1])  # type: str
        object_name = python_object_part_names[-1]  # type: str
        module = importlib.import_module(module_name)
        if not hasattr(module, object_name):
            try:
                importlib.import_module(module_name + "." + object_name)
            except ImportError:
                raise Exception('Cannot find object or module "{module_name}.{object_name}"'
                                .format(object_name=object_name, module_name=module_name))


if __name__ == "__main__":
    assert len(sys.argv) >= 2, "An argument must be specified"
    map(check_if_python_object_exists, sys.argv[1:])
    sys.exit(0)
