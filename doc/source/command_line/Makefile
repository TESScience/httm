.PHONY: all clean
.PRECIOUS: %.md

FILES=command_line.rst command_line.md
DIRECTORIES=scripts/
VENV=../../../test/venv/
PYTHON=$(VENV)/bin/python

all: index.rst

$(VENV):
	make -C $(dir $@) install

$(PYTHON): $(VENV)

index.rst: command_line.rst
	ln -s $< $@

%.rst: %.md
	pandoc --from=markdown --to=rst --output=$@ $<

%.md: create_%_doc.py scripts/ $(PYTHON)
	$(PYTHON) $< > $@

scripts/: ../../../scripts
	@rm -rf $@
	mkdir -p scripts/
	touch scripts/__init__.py
	for script in $</* ; do ln -s ../$${script} scripts/$${script##*/}.py ; done

clean:
	rm -f $(FILES)
	rm -rf $(DIRECTORIES)
