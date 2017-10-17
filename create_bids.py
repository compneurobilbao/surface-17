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

# anat
for file in os.listdir(data_path):
    
    if file.endswith('.nii'):
        subject = file[:-8]
        
        os.makedirs(opj(data_path, 'raw', 'bids', subject, 'ses-001', 'anat'))
        shutil.move(opj(data_path, file), 
                    opj(data_path, 'raw', 'bids', subject, 'ses-001', 'anat'))

# dwi
dwi_data_path = opj(cwd, 'dwi')

for subject in os.listdir(dwi_data_path):
    print(subject)
    try:
        os.makedirs(opj(data_path, 'raw', 'bids', subject, 'ses-001', 'dwi'))
    except:
        pass
    
    shutil.move(opj(dwi_data_path, subject, 'dwi', subject+'_dwi.bval'),
                opj(data_path, 'raw', 'bids', subject, 'ses-001', 'dwi'))
    
    shutil.move(opj(dwi_data_path, subject, 'dwi', subject+'_dwi.bvec'), 
                opj(data_path, 'raw', 'bids', subject, 'ses-001', 'dwi'))
    
    shutil.move(opj(dwi_data_path, subject, 'dwi', subject+'_dwi.nii.gz'), 
                opj(data_path, 'raw', 'bids', subject, 'ses-001', 'dwi'))

# fmri
fmri_data_path = opj(cwd, 'func')

for subject in os.listdir(fmri_data_path):
    print(subject)
    try:
        os.makedirs(opj(data_path, 'raw', 'bids', subject, 'ses-001', 'func'))
    except:
        pass
    
    try:
        shutil.move(opj(fmri_data_path, subject, 'func', subject+'_task-Rest_bold.nii.gz'),
                    opj(data_path, 'raw', 'bids', subject, 'ses-001', 'func'))
        shutil.move(opj(fmri_data_path, subject, 'func', subject+'_task-Rest_bold.json'),
                opj(data_path, 'raw', 'bids', subject, 'ses-001', 'func'))
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
len([f.type for f in files if f.type == 'T1w']) #174 NOT OK
len([f.type for f in files if f.type == 'bold'])/2 #358 NOT OK


