.PHONY: all clean

FILES=calibrated_fits/spot50.fits

all: $(FILES)

calibrated_fits/spot50.fits: ./scripts/make_spot50
	$< $@

clean:
	rm -f $(FILES)
