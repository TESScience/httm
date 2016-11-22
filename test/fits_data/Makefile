.PHONY: all clean
PYTHON=$(CURDIR)/../venv/bin/python
INSTALL=$(CURDIR)/../venv/bin/raw_to_calibrated

FILES=electron_flux_fits/spot50.fits

all: $(FILES)

$(PYTHON):
	make -C .. install

$(INSTALL):
	make -C .. install

electron_flux_fits/spot50.fits: ./scripts/make_spot50
	@make $(PYTHON)
	@make $(INSTALL)
	$(PYTHON) $< $@

clean:
	rm -f $(FILES)
