rm plot.ps comout outp
mcnp6 ip inp=../runWith2Slices.inp notek com=com plotm = plot

# change the plot file to a pdf
ps2pdf plot.ps