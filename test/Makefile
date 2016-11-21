###################### Virtual Environment ######################
.PHONY: install documentation clean test

ifndef DEBUG
QUIET=--quiet
STD_OUT=/dev/null
ERROR_OUT=/dev/null
else
STD_OUT=/dev/stdout
ERROR_OUT=/dev/stderr
endif

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
	@echo -n Installing httm...
	@$(PIP) install $(QUIET) -r requirements.txt --quiet
	@make -C .. clean > $(STD_OUT)
	@(cd .. ; $(PYTHON) setup.py install > $(STD_OUT) 2> $(ERROR_OUT))
	@make -C fits_data/ all > $(STD_OUT)
	@echo done.

$(INSTALL):
	@make install

documentation:
	make -C ../doc {latexpdf,html}

# This is a generic test to make sure that references to python objects in a particular module exist
%-check-type-references: $(VIRTUAL_ENV)
	@make -C ../doc generated-sources > $(STD_OUT)
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
