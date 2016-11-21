###################### Virtual Environment ######################
.PHONY: install documentation clean test

PYTHON_VERSION=3.5
VIRTUAL_ENV=$(CURDIR)/venv
PYTHON=$(VIRTUAL_ENV)/bin/python$(PYTHON_VERSION)
PIP=$(VIRTUAL_ENV)/bin/pip$(PYTHON_VERSION)
RUNIPY=$(VIRTUAL_ENV)/bin/runipy
SITE_PACKAGES=$(VIRTUAL_ENV)/lib/python$(PYTHON_VERSION)/site-packages
VERSION=$(shell python3.5 -c "$(shell grep '^VERSION' $(CURDIR)/../setup.py) ; print(VERSION)")
INSTALL=$(VIRTUAL_ENV)/bin/calibrated_to_raw
TESTS=httm-check-type-references pyfits-check-type-references numpy-check-type-references \
      astropy-check-type-references tutorial-test smoke-test command_line_utilities-test \
      demo-test

all: install

install: $(VIRTUAL_ENV)
	$(PIP) install -r requirements.txt
	make -C .. clean
	(cd .. ; $(PYTHON) setup.py install
	make -C fits_data/ all
	echo done.

$(INSTALL):
	@make install

documentation:
	make -C ../doc {latexpdf,html}

# This is a generic test to make sure that references to python objects in a particular module exist
%-check-type-references: $(VIRTUAL_ENV)
	@make -C ../doc generated-sources
	@echo -n Checking files for broken docstring references for $(patsubst  %-check-type-references,%,$@)...
	@find ../{httm,doc} -name "*.py" \
	| xargs grep -E "\`[\~]?$(patsubst  %-check-type-references,%,$@)" \
	| sed -e "s/.*\`[~]*\($(patsubst  %-check-type-references,%,$@)[^\`]*\)\`.*/\1/" \
	| sort \
	| uniq \
	| xargs $(PYTHON) scripts/python_object_exists.py
	@find ../{httm,doc} -name "*.rst" \
	| xargs grep -E "\`[\~]?$(patsubst  %-check-type-references,%,$@)" \
	| sed -e "s/.*\`[~]*\($(patsubst  %-check-type-references,%,$@)[^\`]*\)\`.*/\1/" \
	| sort \
	| uniq \
	| xargs $(PYTHON) scripts/python_object_exists.py
	@echo OK

test: $(INSTALL)
	@make $(TESTS)

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
