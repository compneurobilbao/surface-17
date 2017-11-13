#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 11:26:37 2017

@author: asier
"""

import os
from os.path import join as opj
import shutil
from bids.grabbids import BIDSLayout


CWD = '/home/asier/git/surface-kljajevic-17'
base_directory = opj(CWD,'data/raw/bids')
out_directory = opj(CWD,'data/output_for_vanja')
layout = BIDSLayout(base_directory)

subjects = layout.get_subjects()
subject_list = ["sub-" + subject for subject in subjects]

#    modalities = ['fa', 'md', 'mo', 'l1', 'radial']


try:
        os.makedirs(opj(data_path, 'raw', 'bids', subject, 'anat'))

for subject in subject_list:
    print(subject)
    try:
        os.makedirs(opj(data_path, 'raw', 'bids', subject, 'anat'))
    except:
        pass
    
    try:
        shutil.copy(opj(anat_data_path, subject, 'anat', subject+'_T1w.nii.gz'),
                    opj(data_path, 'raw', 'bids', subject, 'anat'))
        shutil.move(opj(data_path, subject, 'func',
                    subject+'_task-Rest_bold.json'),
                    opj(data_path, subject, 'func',
                        subject+'_task-rest_bold.json'))
    except:
        pass
  