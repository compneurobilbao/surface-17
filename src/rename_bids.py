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

# fmri
for subject in os.listdir(data_path):
    try:
        shutil.move(opj(data_path, subject, 'func',
                        subject+'_task-Rest_bold.nii.gz'), 
                    opj(data_path, subject,  'func',
                        subject+'_task-rest_bold.nii.gz'))
        shutil.move(opj(data_path, subject, 'func',
                    subject+'_task-Rest_bold.json'), 
                opj(data_path, subject, 'func',
                    subject+'_task-rest_bold.json'))
    except:
        pass