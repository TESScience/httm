###################### Virtual Environment ######################
.PHONY: install test_images documentation clean test version-check

PYTHON_VERSION=2
VIRTUAL_ENV=$(CURDIR)/venv
PYTHON=$(VIRTUAL_ENV)/bin/python$(PYTHON_VERSION)
PIP=$(VIRTUAL_ENV)/bin/pip$(PYTHON_VERSION)
RUNIPY=$(VIRTUAL_ENV)/bin/runipy
SITE_PACKAGES=$(VIRTUAL_ENV)/lib/python$(PYTHON_VERSION)/site-packages
VERSION=$(shell python3.5 -c "$(shell grep '^VERSION' $(CURDIR)/../setup.py) ; print(VERSION)")
INSTALL=$(VIRTUAL_ENV)/bin/raw_to_calibrated
CONFIG_TEST_FITS=output/json_raw.fits output/yaml_raw.fits output/toml_raw.fits output/tsv_raw.fits output/xml_raw.fits \
		 output/toml_calibrated.fits output/json_calibrated.fits output/yaml_calibrated.fits output/tsv_calibrated.fits \
		 output/xml_calibrated.fits
TESTS=version-check httm-check-code-references httm-check-doc-references numpy-check-code-references astropy-check-code-references \
      tutorial-test smoke-test command_line_utilities-test demo-test raw_demo-test order-test $(CONFIG_TEST_FITS)

all: install

install: $(VIRTUAL_ENV)
	$(PIP) install -r requirements.txt
	make -C .. clean
	(cd .. ; $(PYTHON) setup.py install)
	make -C fits_data/ all
	@echo done.

$(INSTALL):
	@make install

documentation:
	make -C ../doc html
	make -C ../doc latexpdf

version-check: $(VIRTUAL_ENV)
	./venv/bin/raw_to_calibrated --version
	./venv/bin/electron_flux_to_raw --version

# This is a generic test to make sure that references to python objects in a particular module exist
%-check-code-references: $(VIRTUAL_ENV)
	@echo -n Checking python source files for broken docstring references for $(patsubst  %-check-code-references,%,$@)...
	@find ../httm -name "*.py" \
	| xargs grep -E "\`[\~]?$(patsubst  %-check-code-references,%,$@)" \
	| sed -e "s/.*\`[~]*\($(patsubst  %-check-code-references,%,$@)[^\`]*\)\`.*/\1/" \
	| sort \
	| uniq \
	| xargs $(PYTHON) scripts/python_object_exists.py
	@echo OK

%-check-doc-references: $(VIRTUAL_ENV)
	@make -C ../doc generated-sources
	@echo -n Checking documentation files for broken docstring references for $(patsubst  %-check-doc-references,%,$@)...
	@find ../doc -name "*.rst" \
	| xargs grep -E "\`[\~]?$(patsubst  %-check-doc-references,%,$@)" \
	| sed -e "s/.*\`[~]*\($(patsubst  %-check-doc-references,%,$@)[^\`]*\)\`.*/\1/" \
	| sort \
	| uniq \
	| xargs $(PYTHON) scripts/python_object_exists.py
	@echo OK

test: $(INSTALL) test_images
	rm -f $(CONFIG_TEST_FITS)
	@make $(TESTS)

test_images:
	make -C fits_data/ clean
	make -C fits_data/

output/:
	mkdir -p $@

output/json_raw.fits: output/ $(VIRTUAL_ENV)
	$(PYTHON) ./venv/bin/electron_flux_to_raw fits_data/electron_flux_fits/spot50.fits $@ --config config/electron_flux_to_raw/config.json

output/yaml_raw.fits: output/ $(VIRTUAL_ENV)
	$(PYTHON) ./venv/bin/electron_flux_to_raw fits_data/electron_flux_fits/spot50.fits $@ --config config/electron_flux_to_raw/config.yaml

output/toml_raw.fits: output/ $(VIRTUAL_ENV)
	$(PYTHON) ./venv/bin/electron_flux_to_raw fits_data/electron_flux_fits/spot50.fits $@ --config config/electron_flux_to_raw/config.toml

output/tsv_raw.fits: output/ $(VIRTUAL_ENV)
	$(PYTHON) ./venv/bin/electron_flux_to_raw fits_data/electron_flux_fits/spot50.fits $@ --config config/electron_flux_to_raw/config.tsv

output/xml_raw.fits: output/ $(VIRTUAL_ENV)
	$(PYTHON) ./venv/bin/electron_flux_to_raw fits_data/electron_flux_fits/spot50.fits $@ --config config/electron_flux_to_raw/config.xml

output/toml_calibrated.fits: output/ $(VIRTUAL_ENV)
	$(PYTHON) ./venv/bin/raw_to_calibrated fits_data/raw_fits/single_ccd.fits $@ --config config/raw_to_calibrated/config.toml

output/json_calibrated.fits: output/ $(VIRTUAL_ENV)
	$(PYTHON) ./venv/bin/raw_to_calibrated fits_data/raw_fits/single_ccd.fits $@ --config config/raw_to_calibrated/config.json

output/yaml_calibrated.fits: output/ $(VIRTUAL_ENV)
	$(PYTHON) ./venv/bin/raw_to_calibrated fits_data/raw_fits/single_ccd.fits $@ --config config/raw_to_calibrated/config.yaml

output/tsv_calibrated.fits: output/ $(VIRTUAL_ENV)
	$(PYTHON) ./venv/bin/raw_to_calibrated fits_data/raw_fits/single_ccd.fits $@ --config config/raw_to_calibrated/config.tsv

output/xml_calibrated.fits: output/ $(VIRTUAL_ENV)
	$(PYTHON) ./venv/bin/raw_to_calibrated fits_data/raw_fits/single_ccd.fits $@ --config config/raw_to_calibrated/config.xml

%-test: notebooks/%.ipynb $(RUNIPY)
	@echo -n Testing $<...
	@$(PYTHON) $(RUNIPY) $(QUIET) $<
	@echo OK
	
$(RUNIPY):
	make install

$(VIRTUAL_ENV):
	virtualenv $(VIRTUAL_ENV_OPTS) --python=python$(PYTHON_VERSION) $@
	@[ -d $@ ]
	@touch $@

clean:
	@make -C fits_data/ clean
	rm -rf $(VIRTUAL_ENV) $(CONFIG_TEST_FITS)
