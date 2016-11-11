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

VIRTUAL_ENV=$(CURDIR)/venv
PYTHON=$(VIRTUAL_ENV)/bin/python2.7
PIP=$(VIRTUAL_ENV)/bin/pip2.7
RUNIPY=$(VIRTUAL_ENV)/bin/runipy
SITE_PACKAGES=$(VIRTUAL_ENV)/lib/python2.7/site-packages
VERSION=$(shell python -c "$(shell grep '^VERSION' $(CURDIR)/../setup.py) ; print VERSION")
INSTALL=$(SITE_PACKAGES)/SPyFFI-$(VERSION)-py2.7.egg
TESTS=httm-check-type-references pyfits-check-type-references numpy-check-type-references \
      astropy-check-type-references plugins-test

all: install

install: $(VIRTUAL_ENV)
	@echo -n Installing httm...
	@echo y | $(PIP) uninstall httm > $(STD_OUT) 2> $(ERROR_OUT) || true
	@$(PIP) install $(QUIET) -r requirements.txt --quiet
	@make -C .. clean > $(STD_OUT)
	@(cd .. ; $(PYTHON) setup.py install > $(STD_OUT) 2> $(ERROR_OUT))
	@echo done.

documentation:
	make -C ../doc {latexpdf,html}

# This is a generic test to make sure that references to python objects exist
%-check-type-references: $(VIRTUAL_ENV)
	@echo -n Checking files for broken docstring references for $(patsubst  %-check-type-references,%,$@)...
	@find ../{httm,doc} -name "*.py" \
	| xargs grep \~$(patsubst  %-check-type-references,%,$@) \
	| sed -e "s/.*~\($(patsubst  %-check-type-references,%,$@)[^ \`]*\)\`.*/\1/" \
	| sort \
	| uniq \
	| xargs $(PYTHON) scripts/python_object_exists.py
	@find ../{httm,doc} -name "*.rst" \
	| xargs grep \~$(patsubst  %-check-type-references,%,$@) \
	| sed -e "s/.*~\($(patsubst  %-check-type-references,%,$@)[^ \`]*\)\`.*/\1/" \
	| sort \
	| uniq \
	| xargs $(PYTHON) scripts/python_object_exists.py
	@echo OK

test: 
	@make $(TESTS)

%-test: %.ipynb $(RUNIPY)
	@echo -n Testing $<...
	@$(PYTHON) $(RUNIPY) $(QUIET) $<
	@echo OK
	
$(RUNIPY):
	make install

$(VIRTUAL_ENV):
	virtualenv --python=python2.7 $@
	@[ -d $@ ]
	@touch $@

clean:
	rm -rf $(VIRTUAL_ENV)
