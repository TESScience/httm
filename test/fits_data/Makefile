.PHONY: all clean
PYTHON=../venv/bin/python
INSTALL=../venv/bin/raw_to_calibrated

FILES=electron_flux_fits/spot50.fits

all: $(FILES)

$(PYTHON) $(INSTALL):
	make -C .. install

electron_flux_fits/spot50.fits: ./scripts/make_spot50
	@make {$(PYTHON),$(INSTALL)}
	$(PYTHON) $< $@

clean:
	rm -f $(FILES)
