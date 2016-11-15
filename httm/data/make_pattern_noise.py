#!/usr/bin/env python
# Create default pattern noise file
from numpy import savez, sin, reshape
amplitude_electrons = 10
pat = reshape(amplitude_electrons*sin(range(2078*2136)), (2078,2136))
savez("pattern_noise.npz", pattern_noise=pat)
