#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 12:10:02 2017

@author: asier
"""

import os
from os.path import join as opj
import shutil
cwd = os.getcwd()

data_path = opj(cwd, 'data', 'raw', 'bids')

# anat
for subject in os.listdir(data_path):   
    try:
        shutil.move(opj(data_path, subject, 'ses-001', 'anat',
                        subject+'_T1w.nii'), 
                    opj(data_path, subject, 'ses-001', 'anat',
                        subject+'_ses-001_T1w.nii'))
    except:
        pass

# dwi
for subject in os.listdir(data_path):
    try:
        shutil.move(opj(data_path, subject, 'ses-001', 'dwi',
                        subject+'_dwi.nii.gz'), 
                    opj(data_path, subject, 'ses-001', 'dwi',
                        subject+'_ses-001_dwi.nii.gz'))
        shutil.move(opj(data_path, subject, 'ses-001', 'dwi',
                    subject+'_dwi.bval'), 
                opj(data_path, subject, 'ses-001', 'dwi',
                    subject+'_ses-001_dwi.bval'))
        shutil.move(opj(data_path, subject, 'ses-001', 'dwi',
                    subject+'_dwi.bvec'), 
                opj(data_path, subject, 'ses-001', 'dwi',
                    subject+'_ses-001_dwi.bvec'))
    except:
        pass

# fmri
for subject in os.listdir(data_path):
    try:
        shutil.move(opj(data_path, subject, 'ses-001', 'func',
                        subject+'_task-Rest_bold.nii.gz'), 
                    opj(data_path, subject, 'ses-001', 'func',
                        subject+'_task-rest_bold.nii.gz'))
        shutil.move(opj(data_path, subject, 'ses-001', 'func',
                    subject+'_task-Rest_bold.json'), 
                opj(data_path, subject, 'ses-001', 'func',
                    subject+'_ses-001_task-rest_bold.json'))
    except:
        pass