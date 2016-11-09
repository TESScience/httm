.PHONY: all documentation test clean

all:

documentation:
	make -C doc {html,latexpdf}

test:
	make -C test/ {install,test}

clean:
	rm -rf build/ dist/ httm.egg-info/ $(shell find httm -name "*.pyc")
