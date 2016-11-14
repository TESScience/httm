"""
``httm.transformations.raw_converters_to_calibrated``
=====================================================

Transformation functions for processing
:py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter` objects so that
they are suitable for writing to a calibrated FITS file.

"""

import raw_slices_to_calibrated


# noinspection PyProtectedMember
def convert_adu_to_electrons(raw_converter):
    # type: (SingleCCDRawConverter) -> SingleCCDRawConverter
    """
    Converts a :py:class:`~httm.data_structures.raw_converter.SingleCCDRawConverter` from
    having *Analogue to Digital Converter Units* (ADU) to estimated electron counts by calling
    :py:func:`~httm.transformations.raw_slices_to_calibrated.convert_slice_adu_to_electrons` over each slice.

    :param raw_converter: Should have ADUs for units for each of its slices
    :type raw_converter: :py:class:`~httm.data_structures.calibrated_converter.SingleCCDCalibratedConverter`
    :rtype: :py:class:`~httm.data_structures.calibrated_converter.SingleCCDCalibratedConverter`
    """
    video_scales = raw_converter.parameters.video_scales
    image_slices = raw_converter.slices
    number_of_exposures = raw_converter.parameters.number_of_exposures
    gain_loss = raw_converter.parameters.gain_loss
    assert len(video_scales) == len(image_slices), "Video scales do not match image slices"
    return raw_converter._replace(
        slices=tuple(
            raw_slices_to_calibrated.convert_slice_adu_to_electrons(
                gain_loss,
                number_of_exposures,
                video_scale,
                image_slice)
            for (video_scale, image_slice) in zip(video_scales, image_slices)))


def remove_pattern_noise(raw_converter):
    # type: (SingleCCDRawConverter) -> SingleCCDRawConverter
    pass


def remove_start_of_line_ringing(raw_converter):
    # type: (SingleCCDRawConverter) -> SingleCCDRawConverter
    pass


def remove_undershoot(raw_converter):
    # type: (SingleCCDRawConverter) -> SingleCCDRawConverter
    pass


def remove_smear(raw_converter):
    # type: (SingleCCDRawConverter) -> SingleCCDRawConverter
    pass
