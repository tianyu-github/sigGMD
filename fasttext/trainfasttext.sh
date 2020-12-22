#!/bin/sh
#SBATCH --partition=GpuPriority                   # Name of partition
#SBATCH --qos=shn15004gpu
#SBATCH --ntasks=18                         # Request 48 CPU cores
#SBATCH --nodes=1
#SBATCH --mail-type=END                      # Event(s) that triggers email notification (BEGIN,END,FAIL,ALL)
#SBATCH --mail-user=<tianyu.wang@uconn.edu>    # Destination email address


cd /home/tiw15008/cleanfiles


module load python/3.5.2

#python trainWord2VecModel4github.py /home/tiw15008/cleanfiles/files2train1/ /home/tiw15008/cleanfiles/fasttextmodel/ fasttext092918 0 none 100 300 18

#python trainWord2VecModel4github.py /home/tiw15008/cleanfiles/files2train/ /home/tiw15008/cleanfiles/fasttextmodel/ fasttext092919 0 none 100 300 18
python trainWord2VecModel4github.py /home/tiw15008/cleanfiles/files2train/ /home/tiw15008/cleanfiles/fasttextmodel/ fasttext100719 1 /home/tiw15008/cleanfiles/bigram.data 100 300 18


#python modeltest.py
