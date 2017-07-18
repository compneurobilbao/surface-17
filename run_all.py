#!/usr/bin/python

# import sys
import os

try:
    os.mkdir(".job/")
    os.mkdir(".out/")
except OSError:
    pass


for file in os.listdir("./data"):
    subject = file[:-4]

    filey = ".job/%s.job" % subject
    filey = open(filey, "w")
    filey.writelines("#!/bin/bash\n")
    filey.writelines("#SBATCH --job-name=%s\n" % subject)
    filey.writelines("#SBATCH --output=.out/%s.out\n" % subject)
    filey.writelines("#SBATCH --error=.out/%s.err\n" % subject)
    filey.writelines("#SBATCH -p large\n")
    filey.writelines("#SBATCH -n 4\n")
    filey.writelines("#SBATCH -N 4\n")
    filey.writelines("#SBATCH --mem=10000\n")
    filey.writelines("\n")

    filey.writelines("module load FreeSurfer/6.0.0-centos6_x86_64\n")
    filey.writelines("source $FREESURFER_HOME/SetUpFreeSurfer.sh\n")
    filey.writelines("export SUBJECTS_DIR=/home/aerramuzpe/surface-kljajevic-17/processed_data\n")
    filey.writelines("recon-all -subjid %s \
                     -i /home/aerramuzpe/surface-kljajevic-17/data/%s \
                     -all \
                     -openmp 4 \
                     -qcache \
                     \n" % (subject, file))
    filey.writelines("module unload FreeSurfer/6.0.0-centos6_x86_64\n")

    filey.close()
    os.system("sbatch  " + ".job/%s.job" % subject)
