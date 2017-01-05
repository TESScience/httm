.PHONY: all clean
PYTHON=$(CURDIR)/../venv/bin/python
INSTALL=$(CURDIR)/../venv/bin/raw_to_calibrated

SPOT50_FITS=electron_flux_fits/spot50.fits
SPOT50_RAW_FITS=raw_fits/spot50_raw.fits
FILES=$(SPOT50_FITS) $(SPOT50_RAW_FITS)

all: $(FILES)

$(PYTHON):
	make -C .. install

$(INSTALL):
	make -C .. install

$(SPOT50_FITS): ./scripts/make_spot50
	@make $(PYTHON)
	@make $(INSTALL)
	$(PYTHON) $< $@

$(SPOT50_RAW_FITS): $(SPOT50_FITS)
	../venv/bin/electron_flux_to_raw --no-add-pattern-noise $< $@

clean:
	rm -f $(FILES)
