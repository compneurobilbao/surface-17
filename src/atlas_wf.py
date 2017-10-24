#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from src.preproc import run_fmriprep

from src.postproc.utils import atlas_to_t1

from src.dmri import (run_dti_artifact_correction,
                      run_spm_fsl_dti_preprocessing,
                      run_camino_tractography,
                      )

from src.dmri.utils import (correct_dwi_space_atlas,
                            )


def main_workflow(SUBJECT_LIST):
    SESSION_LIST = ['ses-001']

    """
    fmriprep and mriqc calls
    """

    run_fmriprep(SUBJECT_LIST, SESSION_LIST)

    # WARNING!! Execute permission change over files before continue
    # sudo chmod 777 -R $OUTPUT_DIR 
    
    
    """
    Atlas to T1w space
    """
    
    atlas_to_t1(SUBJECT_LIST, SESSION_LIST)
    
    """
    dMRI pipeline
    """
    
    run_dti_artifact_correction(SUBJECT_LIST, SESSION_LIST)
    
    run_spm_fsl_dti_preprocessing(SUBJECT_LIST, SESSION_LIST)
    
    correct_dwi_space_atlas(SUBJECT_LIST, SESSION_LIST)
    
    run_camino_tractography(SUBJECT_LIST, SESSION_LIST)

