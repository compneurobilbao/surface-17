#!/usr/bin/python

# import sys
import os

try:
    os.mkdir(".job/")
except OSError:
    pass


for subject_num in range(1, 2515):  # 1 -> n-1
    i = str(subject_num).zfill(3)
    filey = "job/sub-%s.job" % i
    filey = open(filey, "w")
    filey.writelines("#!/bin/bash\n")
    filey.writelines("#SBATCH --job-name=sub-%s\n" % i)
    filey.writelines("#SBATCH --output=.out/sub-%s.out\n" % i)
    filey.writelines("#SBATCH --error=.out/sub-%s.err\n" % i)
    filey.writelines("#SBATCH -p large\n")
    filey.writelines("#SBATCH -n 4\n")
    filey.writelines("#SBATCH -N 4\n")
    filey.writelines("#SBATCH --mem=10000\n")
    filey.writelines("\n")

    filey.writelines("module load FreeSurfer/6.0.0-centos6_x86_64\n")
    filey.writelines("recon-all -subjid sub-%s \
                     -i file%s.nii \
                     -all \
                     -openmp 4 \
                     \n" % (i, i))
    filey.writelines("module unload FreeSurfer/6.0.0-centos6_x86_64\n")

    filey.close()
    os.system("sbatch  " + ".job/%s.job" % i)
