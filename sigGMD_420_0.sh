#!/bin/bash
#SBATCH --partition=general                   # Name of partition
#SBATCH --ntasks=20                           # Request 48 CPU cores
#SBATCH --nodes=1
#SBATCH --time=2:00:00                  # Job should run for up to 2 hours (for example)
#SBATCH --mail-type=END                      # Event(s) that triggers email notification (BEGIN,END,FAIL,ALL)
#SBATCH --mail-user=<tianyu.wang@uconn.edu>    # Destination email address


cd /home/tiw15008/cleanfiles

module load intelics/2012.0.032
module load python/2.7.6
# python hpc_topgene.py
python hpc_topgene_420cell_0.py
