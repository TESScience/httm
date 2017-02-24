Command Line Utilities
======================

``electron_flux_single_ccd_ffi_to_simulated_raw``
-------------------------------------------------

Utility for transforming a FITS with units in electron counts file into
a simulated RAW FITS file

::

    usage: electron_flux_single_ccd_ffi_to_simulated_raw 
           [-h] [--version] [--config CONFIG]
           [--no-introduce-smear-rows]
           [--introduce-smear-rows]
           [--no-add-shot-noise] [--add-shot-noise]
           [--no-simulate-blooming]
           [--simulate-blooming]
           [--no-add-readout-noise]
           [--add-readout-noise]
           [--no-simulate-undershoot]
           [--simulate-undershoot]
           [--no-simulate-start-of-line-ringing]
           [--simulate-start-of-line-ringing]
           [--no-add-baseline] [--add-baseline]
           [--no-convert-electrons-to-adu]
           [--convert-electrons-to-adu]
           [--no-add-pattern-noise]
           [--add-pattern-noise]
           [--number-of-slices NUMBER_OF_SLICES]
           [--camera-number CAMERA_NUMBER]
           [--ccd-number CCD_NUMBER]
           [--number-of-exposures NUMBER_OF_EXPOSURES]
           [--video-scales VIDEO_SCALES [VIDEO_SCALES ...]]
           [--readout-noise-parameters READOUT_NOISE_PARAMETERS [READOUT_NOISE_PARAMETERS ...]]
           [--early-dark-pixel-columns EARLY_DARK_PIXEL_COLUMNS]
           [--late-dark-pixel-columns LATE_DARK_PIXEL_COLUMNS]
           [--final-dark-pixel-rows FINAL_DARK_PIXEL_ROWS]
           [--smear-rows SMEAR_ROWS]
           [--random-seed RANDOM_SEED]
           [--full-well FULL_WELL]
           [--blooming-threshold BLOOMING_THRESHOLD]
           [--gain-loss GAIN_LOSS]
           [--undershoot-parameter UNDERSHOOT_PARAMETER]
           [--single-frame-baseline-adus SINGLE_FRAME_BASELINE_ADUS [SINGLE_FRAME_BASELINE_ADUS ...]]
           [--single-frame-baseline-adu-drift-term SINGLE_FRAME_BASELINE_ADU_DRIFT_TERM]
           [--smear-ratio SMEAR_RATIO]
           [--clip-level-adu CLIP_LEVEL_ADU]
           [--start-of-line-ringing START_OF_LINE_RINGING]
           [--pattern-noise PATTERN_NOISE]
           [--no-smear-rows-present]
           [--smear-rows-present]
           [--no-shot-noise-present]
           [--shot-noise-present]
           [--no-blooming-present] [--blooming-present]
           [--no-readout-noise-present]
           [--readout-noise-present]
           [--no-undershoot-present]
           [--undershoot-present]
           [--no-start-of-line-ringing-present]
           [--start-of-line-ringing-present]
           [--no-pattern-noise-present]
           [--pattern-noise-present]
           [--no-baseline-present] [--baseline-present]
           [--no-in-adu] [--in-adu]
           input output
           

``--help``
~~~~~~~~~~

Print the help message for this command line tool. ### ``--version``
Print the version information. ### ``--config`` Set an optional
configuration file. ### ``--introduce-smear-rows`` /
``--no-introduce-smear-rows`` Introduce *smear rows* to each slice of
the image. ### ``--add-shot-noise`` / ``--no-add-shot-noise`` Add *shot
noise* to each pixel in each slice of the image. ###
``--simulate-blooming`` / ``--no-simulate-blooming`` Simulate *blooming*
on for each column for each slice of the image. ###
``--add-readout-noise`` / ``--no-add-readout-noise`` Add *readout noise*
to each pixel in each slice of the image. ### ``--simulate-undershoot``
/ ``--no-simulate-undershoot`` Simulate *undershoot* on each row of each
slice in the image. ### ``--simulate-start-of-line-ringing`` /
``--no-simulate-start-of-line-ringing`` Simulate *start of line ringing*
on each row of each slice in the image. ### ``--add-baseline`` /
``--no-add-baseline`` Add a *baseline electron count* to each slice in
the image. ### ``--convert-electrons-to-adu`` /
``--no-convert-electrons-to-adu`` Convert the image from having pixel
units in electron counts to *Analogue to Digital Converter Units* (ADU).
### ``--add-pattern-noise`` / ``--no-add-pattern-noise`` Add a fixed
*pattern noise* to each slice in the image. ### ``--number-of-slices``
The number of slices to use in the transformation, either ``1`` or
``4``. ### ``--camera-number`` The number of the camera that took the
image. For real images, the serial number 0-31 of the FPE interface
board is used. ### ``--ccd-number`` The number of the CCD that took the
image. ### ``--number-of-exposures`` The number of frames stacked in the
image. ### ``--video-scales`` The video scaling constants, for
converting back and forth between *Analogue to Digital Converter Units*
(ADU) to electron counts. These have units of electrons per ADU. ###
``--readout-noise-parameters`` The video readout noise standard
deviation in electrons. Corresponds to fluctuations in electron counts
for completely dark pixel data. ### ``--early-dark-pixel-columns`` Count
of columns of pixels that have never traversed the image area or frame
store, and thus were never exposed to light. Read before the image
pixels in the row, these are where most of the start of line ringing may
be seen. ### ``--late-dark-pixel-columns`` Count of columns of pixels
that have never traversed the image area or frame store, and thus were
never exposed to light. Read after the image pixels in a row. ###
``--final-dark-pixel-rows`` Count of rows of pixels that have traversed
the frame store area, but not the image area, and thus were never
exposed to light. ### ``--smear-rows`` Count of rows of pixels that have
traversed the imaging area during frame transfer, but have zero exposure
to light otherwise. These are for estimating the effect of smear on the
imaging pixels. ### ``--random-seed`` The pseudo random number generator
seed. The default value of ``-1`` creates a seed from the system clock.
### ``--full-well`` The expected maximum number of electrons that a
pixel can hold. ### ``--blooming-threshold`` The expected maximum number
of electrons before a pixel blooms. ### ``--gain-loss`` The relative
decrease in video gain over the total ADC range. This is the parameter
of the non-linearity model. This is sometimes referred to as
*compression* in electrical engineering literature. ###
``--undershoot-parameter`` The deficit in a pixel value relative to the
value of its preceding pixel. This is a ratio and dimensionless. The
electronics have a slight memory of the signal level which cause the
pixel following a bright pixel to appear slightly darker that it should.
### ``--single-frame-baseline-adus`` The mean ADU for a pixel with zero
electrons for a single simulated frame exposure, per slice. ###
``--single-frame-baseline-adu-drift-term`` Standard deviation of a
random number added to the single frame baseline adu parameter per
simulated frame (same for all slices). ### ``--smear-ratio`` The time
that a charge packet spends in transit through each imaging pixel that
it does not nominally belong to, relative to the time it spends in the
pixel it does nominally belong to. Used for simulating smear rows. ###
``--clip-level-adu`` The level in ADU where the CCD or the electronics
will clip the video. The default is the maximum the *Analogue to Digital
Converter* (ADC) can deliver. ### ``--start-of-line-ringing`` A vector
to be read from an ``npz`` file, to be added to each row in of a slice,
representing the repeatable change in the video baseline caused by the
disturbance in the data acquisition rhythm between *rows*. Units of the
array are electrons. ### ``--pattern-noise`` A matrix to be read from a
FITS file (either uncompressed or compressed with gzip, bzip2, or
pkzip), representing the repeatable change in the video baseline caused
by the disturbance in the data acquisition rhythm between *frames*.
Organized as a RAW FFI (including dark pixels and smear rows), in
*Analogue to Digital Converter Units* (ADU). ###
``--smear-rows-present`` Flag indicating whether there is data in the
smear rows. ### ``--shot-noise-present`` Flag indicating whether *shot
noise* is present. ### ``--blooming-present`` Flag indicating whether
*blooming* has been simulated. ### ``--readout-noise-present`` Flag
indicating whether *readout noise* is present. ###
``--undershoot-present`` Flag indicating whether *undershoot* is present
or otherwise compensated for. ### ``--start-of-line-ringing-present``
Flag indicating whether *start of line ringing* is present or otherwise
compensated for. ### ``--pattern-noise-present`` Flag indicating whether
*pattern noise* is present or otherwise compensated for. ###
``--baseline-present`` Flag indicating whether a *baseline electron
count* is present or otherwise compensated for. ### ``--in-adu`` Flag
indicating whether the data is in *Analogue to Digital Converter Units*
or otherwise in electron counts. ##
``raw_single_ccd_ffi_to_calibrated_electron_flux`` Transform a RAW FITS
file into a calibrated FITS file with units in electron counts

::

    usage: raw_single_ccd_ffi_to_calibrated_electron_flux 
           [-h] [--version] [--config CONFIG]
           [--no-remove-pattern-noise]
           [--remove-pattern-noise]
           [--no-convert-adu-to-electrons]
           [--convert-adu-to-electrons]
           [--no-remove-baseline] [--remove-baseline]
           [--no-remove-start-of-line-ringing]
           [--remove-start-of-line-ringing]
           [--no-remove-undershoot]
           [--remove-undershoot] [--no-remove-smear]
           [--remove-smear]
           [--number-of-slices NUMBER_OF_SLICES]
           [--camera-number CAMERA_NUMBER]
           [--ccd-number CCD_NUMBER]
           [--number-of-exposures NUMBER_OF_EXPOSURES]
           [--video-scales VIDEO_SCALES [VIDEO_SCALES ...]]
           [--early-dark-pixel-columns EARLY_DARK_PIXEL_COLUMNS]
           [--late-dark-pixel-columns LATE_DARK_PIXEL_COLUMNS]
           [--final-dark-pixel-rows FINAL_DARK_PIXEL_ROWS]
           [--smear-rows SMEAR_ROWS]
           [--gain-loss GAIN_LOSS]
           [--undershoot-parameter UNDERSHOOT_PARAMETER]
           [--pattern-noise PATTERN_NOISE]
           [--no-smear-rows-present]
           [--smear-rows-present]
           [--no-undershoot-present]
           [--undershoot-present]
           [--no-pattern-noise-present]
           [--pattern-noise-present]
           [--no-start-of-line-ringing-present]
           [--start-of-line-ringing-present]
           [--no-baseline-present] [--baseline-present]
           [--no-in-adu] [--in-adu]
           input output
           

``--help``
~~~~~~~~~~

Print the help message for this command line tool. ### ``--version``
Print the version information. ### ``--config`` Set an optional
configuration file. ### ``--remove-pattern-noise`` /
``--no-remove-pattern-noise`` Compensate for a fixed *pattern noise* on
each slice of the image. ### ``--convert-adu-to-electrons`` /
``--no-convert-adu-to-electrons`` Convert the image from having units in
*Analogue to Digital Converter Units* (ADU) to electron counts. ###
``--remove-baseline`` / ``--no-remove-baseline`` Average the pixels in
the dark columns and subtract the result from each pixel in the image.
### ``--remove-start-of-line-ringing`` /
``--no-remove-start-of-line-ringing`` Compensate for *start of line
ringing* on each row of each slice of the image. ###
``--remove-undershoot`` / ``--no-remove-undershoot`` Compensate for
*undershoot* for each row of each slice of the image. ###
``--remove-smear`` / ``--no-remove-smear`` Compensate for *smear* in the
image by reading it from the *smear rows* each slice and removing it
from the rest of the slice. ### ``--number-of-slices`` The number of
slices to use in the transformation, either ``1`` or ``4``. ###
``--camera-number`` The number of the camera that took the image. For
real images, the serial number 0-31 of the FPE interface board is used.
### ``--ccd-number`` The number of the CCD that took the image. ###
``--number-of-exposures`` The number of frames stacked in the image. ###
``--video-scales`` The video scaling constants, for converting back and
forth between *Analogue to Digital Converter Units* (ADU) to electron
counts. These have units of electrons per ADU. ###
``--early-dark-pixel-columns`` Count of columns of pixels that have
never traversed the image area or frame store, and thus were never
exposed to light. Read before the image pixels in the row, these are
where most of the start of line ringing may be seen. ###
``--late-dark-pixel-columns`` Count of columns of pixels that have never
traversed the image area or frame store, and thus were never exposed to
light. Read after the image pixels in a row. ###
``--final-dark-pixel-rows`` Count of rows of pixels that have traversed
the frame store area, but not the image area, and thus were never
exposed to light. ### ``--smear-rows`` Count of rows of pixels that have
traversed the imaging area during frame transfer, but have zero exposure
to light otherwise. These are for estimating the effect of smear on the
imaging pixels. ### ``--gain-loss`` The relative decrease in video gain
over the total ADC range. This is the parameter of the non-linearity
model. This is sometimes referred to as *compression* in electrical
engineering literature. ### ``--undershoot-parameter`` The deficit in a
pixel value relative to the value of its preceding pixel. This is a
ratio and dimensionless. The electronics have a slight memory of the
signal level which cause the pixel following a bright pixel to appear
slightly darker that it should. ### ``--pattern-noise`` A matrix to be
read from a FITS file (either uncompressed or compressed with gzip,
bzip2, or pkzip), representing the repeatable change in the video
baseline caused by the disturbance in the data acquisition rhythm
between *frames*. Organized as a RAW FFI (including dark pixels and
smear rows), in *Analogue to Digital Converter Units* (ADU). ###
``--smear-rows-present`` Flag indicating whether there is data in the
smear rows. ### ``--undershoot-present`` Flag indicating whether
*undershoot* is present or otherwise compensated for. ###
``--pattern-noise-present`` Flag indicating whether *pattern noise* is
present or otherwise compensated for. ###
``--start-of-line-ringing-present`` Flag indicating whether *start of
line ringing* is present or otherwise compensated for. ###
``--baseline-present`` Flag indicating whether a *baseline electron
count* is present or otherwise compensated for. ### ``--in-adu`` Flag
indicating whether the data is in *Analogue to Digital Converter Units*
or otherwise in electron counts.
