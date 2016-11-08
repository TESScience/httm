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
                      for parameter, data in parameter_dictionary.iteritems()])
