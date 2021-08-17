#!/bin/bash

#SBATCH --job-name=a1_1b
#SBATCH --ntasks=210
#SBATCH --partition=broadwl
#SBATCH --constraint=fdr

# Load Python and MPI modules
module load python/anaconda-2019.03
module load intelmpi/2018.2.199+intel-18.0

for i in {1..20}
do
  mpirun -n $i python3 a1_1b.py >> a1_1b.out
done

