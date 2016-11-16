.PHONY: all documentation test clean

all:
	@make {documentation,test,data}

data:
	make -C httm/data all

documentation:
	make -C doc {clean,html,latexpdf}

test:
	make -C test/ {install,test}

clean:
	rm -rf build/ dist/ httm.egg-info/ $(shell find httm -name "*.pyc")
