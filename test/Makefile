###################### Virtual Environment ######################
.PHONY: install test_images documentation clean test

PYTHON_VERSION=3.5
VIRTUAL_ENV=$(CURDIR)/venv
PYTHON=$(VIRTUAL_ENV)/bin/python$(PYTHON_VERSION)
PIP=$(VIRTUAL_ENV)/bin/pip$(PYTHON_VERSION)
RUNIPY=$(VIRTUAL_ENV)/bin/runipy
SITE_PACKAGES=$(VIRTUAL_ENV)/lib/python$(PYTHON_VERSION)/site-packages
VERSION=$(shell python3.5 -c "$(shell grep '^VERSION' $(CURDIR)/../setup.py) ; print(VERSION)")
INSTALL=$(VIRTUAL_ENV)/bin/raw_to_calibrated
TESTS=httm-check-code-references httm-check-doc-references numpy-check-code-references astropy-check-code-references \
      tutorial-test smoke-test command_line_utilities-test demo-test raw_demo-test

all: install

install: $(VIRTUAL_ENV)
	$(PIP) install -r requirements.txt
	make -C .. clean
	(cd .. ; $(PYTHON) setup.py install)
	make -C fits_data/ all
	echo done.

$(INSTALL):
	@make install

documentation:
	make -C ../doc html
	make -C ../doc latexpdf

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
	@make $(TESTS)

test_images:
	make -C fits_data/ clean
	make -C fits_data/

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
	rm -rf $(VIRTUAL_ENV)
