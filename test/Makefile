###################### Virtual Environment ######################
.PHONY: install clean
VIRTUAL_ENV=$(CURDIR)/venv
PYTHON=$(VIRTUAL_ENV)/bin/python2.7
PIP=$(VIRTUAL_ENV)/bin/pip2.7
SITE_PACKAGES=$(VIRTUAL_ENV)/lib/python2.7/site-packages
VERSION=$(shell python -c "$(shell grep '^VERSION' $(CURDIR)/../setup.py) ; print VERSION")
INSTALL=$(SITE_PACKAGES)/SPyFFI-$(VERSION)-py2.7.egg

install: $(VIRTUAL_ENV)
	@echo y | $(PIP) uninstall httm &> /dev/null || true
	(cd .. ; $(PYTHON) setup.py install)

$(VIRTUAL_ENV):
	virtualenv --python=python2.7 $@
	@[ -d $@ ]
	touch $@

clean:
	rm -rf $(VIRTUAL_ENV)
