#!/bin/bash

#Account and Email Information
#SBATCH -A sulbhamalviya
#SBATCH --mail-type=end
#SBATCH --mail-user=sulbhamalviya@u.boisestate.edu

#SBATCH -J PPO-Training          # job name
#SBATCH -o outputs/results.o%j # output and error file name (%j expands to jobID)
#SBATCH -e outputs/errors.e%j
#SBATCH -n 1               # Run one process
#SBATCH --cpus-per-task=48 # allow job to multithread across all cores
#SBATCH -p gpu            # queue (partition) 
#SBATCH -t 7-00:00:00      # run time (d-hh:mm:ss)
#SBATCH --gres=gpu:1             # request 1 GPU

. ~/.bashrc
conda activate nlp-env

python3 ppo_training_definition.py
