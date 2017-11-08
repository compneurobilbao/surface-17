#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 12:21:22 2017

@author: asier
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 13:55:51 2017

@author: asier
"""
import os
import sys


def FAstats(subject_list, base_directory, out_directory):

        import os



        # Getting the relevant diffusion-weighted data
        templates = dict(dwi='processed/FA_connectome/_subject_id_{subject_id}/resample/{subject_id}_dwi_denoised_edc_reslice.nii.gz',
                         bvecs='raw/bids/{subject_id}/dwi/{subject_id}_dwi.bvec' ,
                         bvals='raw/bids/{subject_id}/dwi/{subject_id}_dwi.bval' ,
                         mask='processed/FA_connectome/_subject_id_{subject_id}/bet/{subject_id}_dwi_denoised_edc_reslice_b0_brain_mask.nii.gz')


def main():
    from os.path import join as opj
    from bids.grabbids import BIDSLayout

    CWD = '/home/asier/git/surface-kljajevic-17'
    base_directory = opj(CWD, 'data/')
    out_directory = opj(CWD, 'data/stats')
    layout = BIDSLayout(base_directory)

    subjects = layout.get_subjects()
    subject_list = ["sub-" + subject for subject in subjects]

    os.chdir(out_directory)
    FAstats(subject_list, base_directory, out_directory)


if __name__ == '__main__':
    # main should return 0 for success, something else (usually 1) for error.
    sys.exit(main())
