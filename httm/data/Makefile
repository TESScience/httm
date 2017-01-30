.PHONY: all clean
FILES=default_pattern_noise.npz default_start_of_line_ringing.npz simulated_pattern.fits

all: $(FILES)

default_%.npz: ./scripts/make_%
	$< $@

simulated_pattern.fits: ./scripts/make_simulated_pattern
	$< $@

clean:
	rm -f $(FILES)
