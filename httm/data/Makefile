.PHONY: all clean
FILES=default_start_of_line_ringing.npz simulated_pattern_noise.fits

all: $(FILES)

default_%.npz: ./scripts/make_%
	$< $@

simulated_pattern_noise.fits: ./scripts/make_simulated_pattern_noise
	$< $@

clean:
	rm -f *.fits *.npz $(FILES)
