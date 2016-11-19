.PHONY: all clean

FILES=electron_flux_fits/spot50.fits

all: $(FILES)

electron_flux_fits/spot50.fits: ./scripts/make_spot50
	$< $@

clean:
	rm -f $(FILES)
