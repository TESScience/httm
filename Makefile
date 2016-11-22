.PHONY: all documentation test clean

all:
	@make {documentation,test,data}

data:
	make -C httm/data all

documentation:
	make -C doc/ clean
	make -C doc/ html
	make -C doc/ latexpdf

test:
	make -C test/ install
	make -C test/ test

clean:
	rm -rf build/ dist/ httm.egg-info/ $(shell find httm -name "*.pyc")
