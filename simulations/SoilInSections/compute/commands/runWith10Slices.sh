#!/bin/bash

#SBATCH --job-name=runWith10Slices
#SBATCH --account=auburn-mins
##SBATCH -p medium
##SBATCH --account=scinet
#SBATCH --mail-type=ALL # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=jose.cortes2@mavs.uta.edu
#SBATCH --nodes=1
#SBATCH --exclusive

#SBATCH --cpus-per-task=48

##SBATH -p priority --qos=nsdl
#SBATCH --time=200:00:00

atlas=true
line=runWith10Slices
n_tasks=90

echo ########
echo 'Running' $line
echo ########
echo ''
date

input_file=input/$line.inp

outp=output/outp/$line.outp
runtpe=output/runtpe/$line.runtpe
mctal=output/mctal/$line.mctal
ptrac=output/ptrac/$line.ptrac


rm $outp $mctal $runtpe #$ptrac
echo 'Starting' $line

start_time=$(date +%s)

if [ $atlas = true ]; then
    module load apptainer 
    apptainer exec --pem-path=/home/jose.cortes/.ssh/mkey-pub.pem /apps/licensed/mcnp/mcnp-encrypted.sif mcnp6 r i=$input_file o=$outp mctal=$mctal ru=$runtpe notek tasks $n_tasks
else
    mcnp6 r i=$input_file o=$outp mctal=$mctal ru=$runtpe notek tasks $n_tasks
fi

end_time=$(date +%s)
## diagnostics
# write the simulation time to a file
echo $line $(($end_time - $start_time)) >> output/sim_times.txt
echo ''
date
echo ''