.PHONY: all clean
FILES=pattern_noise.npz start_of_line_ringing.npz

all: $(FILES)

%.npz: ./scripts/make_%
	$< $@

clean:
	rm -f $(FILES)
