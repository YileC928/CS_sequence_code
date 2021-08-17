#!/bin/bash
#SBATCH --job-name=gpu   # job name
#SBATCH --output=a1_3c10.out # output log file
#SBATCH --error=a1_3c10.err  # error file
#SBATCH --time=00:01:00  # 1 minutes of wall time
#SBATCH --nodes=1        # 1 GPU node
#SBATCH --partition=gpu2 # GPU2 partition
#SBATCH --ntasks=1       # 1 CPU core to drive GPU
#SBATCH --gres=gpu:1     # Request 1 GPU
#SBATCH --mem-per-cpu=8G

module load cuda
module load python/anaconda-2019.03

python3 ./a1_3c10.py
