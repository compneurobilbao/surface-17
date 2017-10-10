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
    
    shutil.move(opj(fmri_data_path, subject, 'func', subject+'_task-Rest_bold.nii.gz'),
                opj(data_path, 'raw', 'bids', subject, 'ses-001', 'func'))
    shutil.move(opj(fmri_data_path, subject, 'func', subject+'_task-Rest_bold.json'),
            opj(data_path, 'raw', 'bids', subject, 'ses-001', 'func'))
    