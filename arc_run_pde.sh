#!/bin/bash

# Execute me from terminal to run the sub-grid model, simulate me in multiple realisations thus forming an ensemble.
# Run: 'qsub run_sgm.sh' on leeds HPC to use a task array of n cores.
# either on the HPC or locally.

###########__________Run script__________#############
################ Hpc machine ################

module load python/3.6.5
module load python-libs/3.1.0

#$ -cwd -V
#$ -l h_rt=48:00:00
#$ -t 1-1

python3 run_pde_HPC.py $SGE_TASK_ID
