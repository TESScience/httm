###################### Virtual Environment ######################
.PHONY: install documentation clean
HTML_DOCUMENTATION=../doc/build/html/index.html
VIRTUAL_ENV=$(CURDIR)/venv
PYTHON=$(VIRTUAL_ENV)/bin/python2.7
PIP=$(VIRTUAL_ENV)/bin/pip2.7
SITE_PACKAGES=$(VIRTUAL_ENV)/lib/python2.7/site-packages
VERSION=$(shell python -c "$(shell grep '^VERSION' $(CURDIR)/../setup.py) ; print VERSION")
INSTALL=$(SITE_PACKAGES)/SPyFFI-$(VERSION)-py2.7.egg

all: install

install: $(VIRTUAL_ENV)
	@echo y | $(PIP) uninstall httm &> /dev/null || true
	@$(PIP) install -r requirements.txt --quiet
	(cd .. ; $(PYTHON) setup.py install)

documentation: $(HTML_DOCUMENTATION)

$(HTML_DOCUMENTATION):
	make -C ../docs html

$(VIRTUAL_ENV):
	virtualenv --python=python2.7 $@
	@[ -d $@ ]
	touch $@

clean:
	rm -rf $(VIRTUAL_ENV)
