"""
``httm.transformations.raw_converters_to_calibrated``
=====================================================

Transformation functions for processing
:py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter` objects so that
they are suitable for writing to a calibrated FITS file.

"""

import raw_slices_to_calibrated


# noinspection PyProtectedMember
def convert_adu_to_electrons(raw_transformation):
    # type: (SingleCCDRawConverter) -> SingleCCDRawConverter
    """
    Converts a :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter` from
    having *Analogue to Digital Converter Units* (ADU) to estimated electron counts by calling
    :py:func:`~httm.transformations.raw_slices_to_calibrated.convert_slice_adu_to_electrons` over each slice.

    :param raw_transformation: Should have ADUs for units for each of its slices
    :type raw_transformation: :py:class:`~httm.data_structures.calibrated_converter.SingleCCDCalibratedConverter`
    :rtype: :py:class:`~httm.data_structures.calibrated_converter.SingleCCDCalibratedConverter`
    """
    video_scales = raw_transformation.parameters.video_scales
    image_slices = raw_transformation.slices
    number_of_exposures = raw_transformation.parameters.number_of_exposures
    gain_loss = raw_transformation.parameters.gain_loss
    assert len(video_scales) == len(image_slices), "Video scales do not match image slices"
    return raw_transformation._replace(
        slices=tuple(
            raw_slices_to_calibrated.convert_slice_adu_to_electrons(
                gain_loss,
                number_of_exposures,
                video_scale,
                image_slice)
            for (video_scale, image_slice) in zip(video_scales, image_slices)))
