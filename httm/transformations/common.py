"""
``httm.transformations.common``
===============================

Common transformations functions used in processing either calibrated or RAW FITS images.
"""


def map_slice_transformation_over_converter(slice_transformation, converter, flag_name=None, flag_status=None):
    """
    Map a function that takes a slice and outputs a slice over an object which is either a
    :py:class:`~httm.data_structures.calibrated_converter.CalibratedConverter`
    or a :py:class:`~httm.data_structures.raw_converter.RAWConverter`.

    Optionally, set a flag on the converter if `flag_name` is specified to `flag_status`.
    If the flag is already set to that status, this function will throw.

    :param slice_transformation: A function that transforms a :py:class:`~httm.data_structures.common.Slice`.
    :type slice_transformation: (:py:class:`~httm.data_structures.common.Slice`) -> \
    :py:class:`~httm.data_structures.common.Slice`
    :param converter: Either a *RAW to Calibrated* or *Calibrated to RAW* converter object, containing slices\
    to be transformed.
    :type converter: :py:class:`~httm.data_structures.calibrated_converter.CalibratedConverter` or \
    :py:class:`~httm.data_structures.raw_converter.RAWConverter`
    :param flag_name: A flag name specified in either \
    :py:class:`~httm.data_structures.calibrated_converter.CalibratedConverterFlags` or \
    :py:class:`~httm.data_structures.raw_converter.RAWConverterFlags`
    :type flag_name: str
    :param flag_status: The status to set the flag to after the transformation.  If the flag is already set,\
    this throws.
    :type flag_status: bool
    :rtype: :py:class:`~httm.data_structures.calibrated_converter.CalibratedConverter` or \
    :py:class:`~httm.data_structures.raw_converter.RAWConverter`
    """
    assert flag_name is None or hasattr(converter.flags, flag_name) and isinstance(flag_status, bool), \
        "Flag {flag_name} must be an attribute of the " \
        "CalibratedConverterFlags object and its status must be boolean".format(flag_name=flag_name)
    assert flag_name is None or getattr(converter.flags, flag_name) != flag_status, \
        "Flag {flag_name} is already set to {flag_status}".format(flag_name=flag_name, flag_status=flag_status)
    # noinspection PyProtectedMember
    return converter._replace(
        slices=tuple(slice_transformation(s) for s in converter.slices),
        flags=converter.flags if (flag_name is None) else
        converter.flags._replace(**{flag_name: flag_status})
    )
