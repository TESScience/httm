.PHONY: all test clean

all:

test:
	make -C test/ {install,test}

clean:
	rm -rf build/ dist/ httm.egg-info/ $(shell find httm -name "*.pyc")
