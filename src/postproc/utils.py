#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 17 11:23:57 2017

@author: asier
"""
from src.env import DATA, ATLAS_TYPES, NEIGHBOURS, ELECTRODE_SPHERE_SIZE

import os
import os.path as op
from os.path import join as opj
import numpy as np
import nibabel as nib
import subprocess

PROCESSED = opj(DATA, 'processed', 'fmriprep')
EXTERNAL = opj(DATA, 'external')
EXTERNAL_MNI_09c = opj(EXTERNAL, 'standard_mni_asym_09c')


def execute(cmd):
    popen = subprocess.Popen(cmd,
                             stdout=subprocess.PIPE,
                             universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


def scrubbing(time_series, FD, thres=0.2):
    """
    simple scrubbing strategy based on timepoint removal
    """
    scrubbed_time_series = time_series.T[:, (FD < thres)]
    return scrubbed_time_series.T


def atlas_to_t1(sub):
    """
    Atlas to T1w space
    """

    # Extract brain from subject space
    command = ['fslmaths',
               opj(PROCESSED, sub, 'anat',
                   sub + '_T1w_preproc.nii.gz'),
               '-mas',
               opj(PROCESSED, sub, 'anat',
                   sub + '_T1w_brainmask.nii.gz'),
               opj(PROCESSED, sub, 'anat',
                   sub + '_T1w_brain.nii.gz'),
               ]
    for output in execute(command):
        print(output)

    # Brain 09c -> Brain subject (save omat)
    command = ['flirt',
               '-in',
               opj(EXTERNAL_MNI_09c,
                   'mni_icbm152_t1_tal_nlin_asym_09c_brain.nii'),
               '-ref',
               opj(PROCESSED, sub, 'anat',
                   sub + '_T1w_brain.nii.gz'),
               '-omat',
               opj(PROCESSED, sub, 'anat',
                   '09c_2_' + sub  + '.mat'),
               ]
    for output in execute(command):
        print(output)

    for atlas in ATLAS_TYPES:
        # Atlas 09c -> Subject space (using previous omat)
        command = ['flirt',
                   '-in',
                   opj(EXTERNAL,
                       'bha_' + atlas + '_1mm_mni09c.nii.gz'),
                   '-ref',
                   opj(PROCESSED, sub, 'anat',
                       sub + '_T1w_brain.nii.gz'),
                   '-out',
                   opj(PROCESSED, sub, 'anat',
                       sub + '_' + atlas + '.nii.gz'),
                   '-init',
                   opj(PROCESSED, sub, 'anat',
                       '09c_2_' + sub + '.mat'),
                   '-applyxfm', '-interp', 'nearestneighbour',
                   ]
        for output in execute(command):
            print(output)
        atlas_with_all_rois(sub, atlas, opj(PROCESSED, sub,
                                            'anat', sub + '_' + atlas +
                                            '.nii.gz'))

    return


def atlas_with_all_rois(sub, atlas, atlas_new):
    """
    Function to correct atlas after resampling (looses some rois),
    this function recovers those lost rois
    """

    atlas_old = opj(EXTERNAL, 'bha_' + atlas + '_1mm_mni09c.nii.gz')
#    atlas_new = opj(PROCESSED, sub, ses, 'func', sub + '_' + ses +
#                    '_' + atlas + '_bold_space.nii.gz')

    atlas_new_img = nib.load(atlas_new)
    m = atlas_new_img.affine[:3, :3]

    atlas_old_data = nib.load(atlas_old).get_data()
    atlas_old_data_rois = np.unique(atlas_old_data)
    atlas_new_data = atlas_new_img.get_data()
    atlas_new_data_rois = np.unique(atlas_new_data)

    diff_rois = np.setdiff1d(atlas_old_data_rois, atlas_new_data_rois)

    for roi in diff_rois:
        p = np.argwhere(atlas_old_data == roi)[0]
        x, y, z = (np.round(np.diag(np.divide(p, m)))).astype(int)
        atlas_new_data[x, y, z] = roi

    atlas_new_data_img_corrected = nib.Nifti1Image(atlas_new_data,
                                                   affine=atlas_new_img.affine)

    nib.save(atlas_new_data_img_corrected,
             atlas_new)
