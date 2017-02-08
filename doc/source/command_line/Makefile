.PHONY: all clean
.PRECIOUS: %.md

FILES=command_line.rst command_line.md venv
DIRECTORIES=scripts/
PYTHON=venv/bin/python

all: command_line.rst

../../../test/venv/:
	make -C $(dir $@) install

venv/: ../../../test/venv/
	@rm -f $@
	ln -s $< $@

%.rst: %.md
	pandoc --from=markdown --to=rst --output=$@ $<

%.md: create_%_doc.py venv/ scripts/
	$(PYTHON) $< > $@

scripts/: ../../../scripts
	@rm -rf $@
	mkdir -p scripts/
	touch scripts/__init__.py
	for script in $</* ; do ln -s ../$${script} scripts/$${script##*/}.py ; done

clean:
	rm -f $(FILES)
	rm -rf $(DIRECTORIES)
