#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 11:29:16 2017

@author: asier
"""

import os
from os.path import join as opj
import shutil
cwd = os.getcwd()

data_path = opj(cwd, 'data')
src_data_path = '/home/asier/Desktop/CamCan'
# anat
anat_data_path = opj(src_data_path, 'anat')

for subject in os.listdir(anat_data_path):
    print(subject)
    try:
        os.makedirs(opj(data_path, 'raw', 'bids', subject, 'anat'))
    except:
        pass
    
    try:
        shutil.move(opj(anat_data_path, subject, 'anat', subject+'_T1w.nii'),
                    opj(data_path, 'raw', 'bids', subject, 'anat'))
    except:
        pass
  
    try:
        shutil.move(opj(anat_data_path, subject, 'anat', subject+'_T1w.json'), 
                    opj(data_path, 'raw', 'bids', subject, 'anat'))
    except:
        pass

# dwi
dwi_data_path = opj(src_data_path, 'dwi')

for subject in os.listdir(dwi_data_path):
    print(subject)
    try:
        os.makedirs(opj(data_path, 'raw', 'bids', subject, 'dwi'))
    except:
        pass
    
    shutil.move(opj(dwi_data_path, subject, 'dwi', subject+'_dwi.bval'),
                opj(data_path, 'raw', 'bids', subject, 'dwi'))
    
    shutil.move(opj(dwi_data_path, subject, 'dwi', subject+'_dwi.bvec'), 
                opj(data_path, 'raw', 'bids', subject, 'dwi'))
    
    shutil.move(opj(dwi_data_path, subject, 'dwi', subject+'_dwi.nii.gz'), 
                opj(data_path, 'raw', 'bids', subject, 'dwi'))

# fmri
fmri_data_path = opj(src_data_path, 'func')

for subject in os.listdir(fmri_data_path):
    print(subject)
    try:
        os.makedirs(opj(data_path, 'raw', 'bids', subject, 'func'))
    except:
        pass
    
    try:
        shutil.move(opj(fmri_data_path, subject, 'func', subject+'_task-Rest_bold.nii.gz'),
                    opj(data_path, 'raw', 'bids', subject, 'func'))
        shutil.move(opj(fmri_data_path, subject, 'func', subject+'_task-Rest_bold.json'),
                opj(data_path, 'raw', 'bids', subject, 'func'))
    except Exception as e:
        print(e)
        pass


"""
Correct uploading checking
"""
import os
from os.path import join as opj
import shutil
cwd = '/home/asier/Desktop/CamCan'

# LOCAL 
anat_data_path = opj(cwd, 'anat')
print(len(os.listdir(anat_data_path)))

dwi_data_path = opj(cwd, 'dwi')
print(len(os.listdir(dwi_data_path)))

fmri_data_path = opj(cwd, 'func')
print(len(os.listdir(fmri_data_path)))


# Cluster
import os
from os.path import join as opj
from bids.grabbids import BIDSLayout

cwd = os.getcwd()
bids_path = opj(cwd, 'data', 'raw', 'bids')

layout = BIDSLayout(bids_path)
files = layout.get(target='type')
len([f.type for f in files if f.type == 'dwi'])/3 #648 OK
len([f.type for f in files if f.type == 'T1w' and 'gz' in f.filename ]) #652 partially OK
len([f.type for f in files if f.type == 'bold' and 'rest' in f.filename])/2 #647.5 partially OK
