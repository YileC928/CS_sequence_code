#!/bin/bash

#SBATCH --job-name=a1_1a
#SBATCH --ntasks=1
#SBATCH --partition=broadwl
#SBATCH --constraint=fdr

# Load Python and MPI modules
module load python/anaconda-2019.03
module load intelmpi/2018.2.199+intel-18.0

python3 a1_1a.py

