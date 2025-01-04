rm plot.ps comout outp
mcnp6 ip inp=../runWith1000Slices.inp notek com=com plotm = plot

# change the plot file to a pdf
ps2pdf plot.ps

# change the pdf to a png
convert -density 300 plot.pdf -quality 90 plot.png

