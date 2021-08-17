#!/bin/bash
#SBATCH --job-name=gpu   # job name
#SBATCH --output=a1_3a.out # output log file
#SBATCH --error=a1_3a.err  # error file
#SBATCH --time=00:02:00  # 2 minutes of wall time
#SBATCH --nodes=1        # 1 GPU node
#SBATCH --partition=gpu2 # GPU2 partition
#SBATCH --ntasks=1       # 1 CPU core to drive GPU
#SBATCH --gres=gpu:1     # Request 1 GPU

module load cuda
module load python/anaconda-2019.03
python3 ./a1_3a.py
