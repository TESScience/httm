.PHONY: all clean
FILES=default_pattern_noise.npz default_start_of_line_ringing.npz

all: $(FILES)

default_%.npz: ./scripts/make_%
	$< $@

clean:
	rm -f $(FILES)
