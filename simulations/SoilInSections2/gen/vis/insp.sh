
# write the above in a for loop to run for all the input files
# there is a file at '../inp/filenames.csv' with the names of the input files
for i in $(tail -n +2 ../inp/filenames.csv); do
    rm plot.ps comout outp
    mcnp6 ip inp=../../compute/input/$i.inp notek com=com plotm = plot
    ps2pdf plot.ps
    convert -density 300 plot.pdf -quality 90 ../../data/vis/$i.png
done
