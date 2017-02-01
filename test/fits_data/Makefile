.PHONY: all clean
PYTHON=$(CURDIR)/../venv/bin/python
INSTALL=$(CURDIR)/../venv/bin/raw_to_calibrated

SPOT50_FITS=electron_flux_fits/spot50.fits
SPOT50_CALIBRATED_FITS=electron_flux_fits/spot50_calibrated.fits
SPOT50_PATTERN_NOISE_FITS=raw_fits/spot50_PATTERN_NOISE.fits
SPOT50_PATTERN_NOISE_FITS_GZIP=raw_fits/spot50_PATTERN_NOISE.fits.gz
SPOT50_RAW_FITS=raw_fits/spot50_raw.fits
SAMPLE_RAW_FITS=raw_fits/sample_raw.fits
SAMPLE_CALIBRATED_FITS=electron_flux_fits/sample_calibrated.fits
FILES=$(SPOT50_FITS) $(SPOT50_RAW_FITS) \
      $(SPOT50_PATTERN_NOISE_FITS) \
      $(SPOT50_PATTERN_NOISE_FITS_GZIP) \
      $(SPOT50_CALIBRATED_FITS) \
      $(SAMPLE_RAW_FITS) \
      $(SAMPLE_CALIBRATED_FITS)

all: $(FILES)

$(PYTHON):
	make -C .. install

$(INSTALL):
	make -C .. install

$(SPOT50_FITS): ./scripts/make_spot50
	@make $(PYTHON)
	@make $(INSTALL)
	$(PYTHON) $< $@

$(SPOT50_PATTERN_NOISE_FITS): ./scripts/make_spot50_pattern $(SPOT50_FITS)
	$(PYTHON) $< $@

$(SPOT50_PATTERN_NOISE_FITS_GZIP): $(SPOT50_PATTERN_NOISE_FITS)
	rm -f $@
	gzip $<

$(SPOT50_RAW_FITS): $(SPOT50_FITS) $(SPOT50_PATTERN_NOISE_FITS_GZIP)
	LOG=DEBUG $(PYTHON) ../venv/bin/electron_flux_to_raw --pattern-noise $(SPOT50_PATTERN_NOISE_FITS_GZIP) $< $@

$(SPOT50_CALIBRATED_FITS): $(SPOT50_RAW_FITS) $(SPOT50_PATTERN_NOISE_FITS_GZIP)
	LOG=DEBUG $(PYTHON) ../venv/bin/raw_to_calibrated --pattern-noise $(SPOT50_PATTERN_NOISE_FITS_GZIP) $< $@

$(SAMPLE_RAW_FITS): electron_flux_fits/sample_electrons.fits
	LOG=DEBUG $(PYTHON) ../venv/bin/electron_flux_to_raw $< $@

$(SAMPLE_CALIBRATED_FITS): $(SAMPLE_RAW_FITS)
	LOG=DEBUG $(PYTHON) ../venv/bin/raw_to_calibrated $< $@

clean:
	rm -f $(FILES)
