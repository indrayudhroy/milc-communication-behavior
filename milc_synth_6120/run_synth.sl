#!/bin/bash -l

#SBATCH -N 204		#Use 204 nodes
#SBATCH -p regular	#Submit to the regular 'partition'
#SBATCH -L SCRATCH	#Job requires $SCRATCH file system
#SBATCH -C haswell 	#Use Haswell nodes
#SBATCH -S 2		#Core specialization = 2
#SBATCH -t 00:30:00

module load craype-hugepages2M

srun -n 6120 -c 2 --cpu-freq=2300000 ./milc_synth
