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
base_directory = opj(CWD, 'data/raw/bids')
input_directory = opj(CWD, 'data/processed/FA_connectome')
out_directory = opj(CWD, 'data/output_for_vanja')
layout = BIDSLayout(base_directory)

subjects = layout.get_subjects()
subject_list = ["sub-" + subject for subject in subjects]

#    modalities = ['fa', 'md', 'mo', 'l1', 'radial']


try:
    os.makedirs(opj(out_directory, 'fa'))
    os.makedirs(opj(out_directory, 'md'))
    os.makedirs(opj(out_directory, 'mo'))
    os.makedirs(opj(out_directory, 'l1'))
    os.makedirs(opj(out_directory, 'radial'))
except:
    pass


for subject in subject_list:
    print(subject)
    # FA
    try:
        shutil.move(opj(input_directory,
                        '_subject_id_' + subject,
                        'flt_fa',
                        'dtifit__FA_flirt.nii.gz'),
                    opj(out_directory, 'fa', subject+'_fa.nii.gz'))
    except:
        pass

    # MD
    try:
        shutil.move(opj(input_directory,
                        '_subject_id_' + subject,
                        'flt_md',
                        'dtifit__MD_flirt.nii.gz'),
                    opj(out_directory, 'md', subject+'_md.nii.gz'))
    except:
        pass

    # MO
    try:
        shutil.move(opj(input_directory,
                        '_subject_id_' + subject,
                        'flt_mo',
                        'dtifit__MO_flirt.nii.gz'),
                    opj(out_directory, 'mo', subject+'_mo.nii.gz'))
    except:
        pass

    # L1 - Axial
    try:
        shutil.move(opj(input_directory,
                        '_subject_id_' + subject,
                        'flt_l1',
                        'dtifit__L1_flirt.nii.gz'),
                    opj(out_directory, 'l1', subject+'_l1.nii.gz'))
    except:
        pass

    # Radial
    try:
        shutil.move(opj(input_directory,
                        '_subject_id_' + subject,
                        'flt_rad',
                        'radial_diff_flirt.nii.gz'),
                    opj(out_directory, 'radial', subject+'_radial.nii.gz'))
    except:
        pass
