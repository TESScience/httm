#!/usr/bin/env python
#Create default start of line ringing file
from numpy import linspace, concatenate, savez, array
#T his zero-pads the ringing, makes a line for standard TESS format. 
# Units are electrons, although the linspace approximation came from
# inspecting an ADU plot of real data.
video_scale=5.2
solr1=video_scale*concatenate((
	linspace(-0.6,0.4,num=40),
	linspace(0.4,-0.4,40),
	linspace(-0.4,0.0,20),
	linspace(0.0,0.0,434)))
savez("solr.npz", start_of_line_ringing=array([solr1,solr1,solr1,solr1]))
