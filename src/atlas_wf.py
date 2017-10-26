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


def main_workflow(sub):
    """
    fmriprep and mriqc calls
    """
    run_fmriprep(sub[0])

    # WARNING!! Execute permission change over files before continue
    # sudo chmod 777 -R $OUTPUT_DIR 
    
    
#    """
#    Atlas to T1w space
#    """
#    
#    atlas_to_t1(sub)
#    
#    """
#    dMRI pipeline
#    """
#    
#    run_dti_artifact_correction(sub)
#    
#    run_spm_fsl_dti_preprocessing(sub)
#    
#    correct_dwi_space_atlas(sub)
#    
#    run_camino_tractography(sub)
#
