#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 13:55:51 2017

@author: asier
"""
import os
import sys


def DTmeasures2std(subject_list, base_directory, out_directory):

        # ==================================================================
        # Loading required packages
        import nipype.pipeline.engine as pe
        import nipype.interfaces.utility as util
        import nipype.interfaces.fsl as fsl

        from nipype import SelectFiles
        import os

        # Getting the subject ID
        infosource = pe.Node(interface=util.IdentityInterface(
            fields=['subject_id']), name='infosource')
        infosource.iterables = ('subject_id', subject_list)

        # Getting the relevant diffusion-weighted data
        templates = dict(dwi='processed/FA_connectome/_subject_id_{subject_id}/resample/{subject_id}_dwi_denoised_edc_reslice.nii.gz',
                         bvecs='raw/bids/{subject_id}/dwi/{subject_id}_dwi.bvec' ,
                         bvals='raw/bids/{subject_id}/dwi/{subject_id}_dwi.bval' ,
                         mask='processed/FA_connectome/_subject_id_{subject_id}/bet/{subject_id}_dwi_denoised_edc_reslice_b0_brain_mask.nii.gz')

        selectfiles = pe.Node(SelectFiles(templates),
                              name='selectfiles')
        selectfiles.inputs.base_directory = os.path.abspath(base_directory)

        dti = pe.Node(interface=fsl.DTIFit(),
                      name='dti')
        calc_radial = pe.Node(interface=fsl.MultiImageMaths(op_string='-add %s -div 2',
                                                            out_file='radial_diff.nii.gz'))
        # FA to Standard
        flt_fa = pe.Node(interface=fsl.FLIRT(dof=12,
                                             cost_func='mutualinfo',
                                             reference ='/usr/share/fsl/5.0/data/standard/MNI152_T1_1mm_brain.nii.gz'),
                         name='flt_fa')

        flt_md = pe.Node(interface=fsl.FLIRT(dof=12,
                                             cost_func='mutualinfo',
                                             reference ='/usr/share/fsl/5.0/data/standard/MNI152_T1_1mm_brain.nii.gz'),
                         name='flt_md')

        flt_mo = pe.Node(interface=fsl.FLIRT(dof=12,
                                             cost_func='mutualinfo',
                                             reference ='/usr/share/fsl/5.0/data/standard/MNI152_T1_1mm_brain.nii.gz'),
                         name='flt_mo')

        flt_l1 = pe.Node(interface=fsl.FLIRT(dof=12,
                                             cost_func='mutualinfo',
                                             reference ='/usr/share/fsl/5.0/data/standard/MNI152_T1_1mm_brain.nii.gz'),
                         name='flt_l1')

        flt_rad = pe.Node(interface=fsl.FLIRT(dof=12,
                                              cost_func='mutualinfo',
                                              reference ='/usr/share/fsl/5.0/data/standard/MNI152_T1_1mm_brain.nii.gz'),
                          name='flt_rad')

        # ==================================================================
        # Setting up the workflow
        DTmeasures2std = pe.Workflow(name='DTmeasures2std')

        # Reading in files
        DTmeasures2std.connect(infosource, 'subject_id',
                               selectfiles, 'subject_id')

        # Calc measures
        DTmeasures2std.connect(selectfiles, 'dwi',
                               dti, 'dwi')
        DTmeasures2std.connect(selectfiles, 'bvecs',
                               dti, 'bvecs')
        DTmeasures2std.connect(selectfiles, 'bvals',
                               dti, 'bvals')
        DTmeasures2std.connect(selectfiles, 'mask',
                               dti, 'mask')
        # Calc radial diff
        DTmeasures2std.connect(dti, 'L2',
                               calc_radial, 'in_file')
        DTmeasures2std.connect(dti, 'L3',
                               calc_radial, 'operand_files')

        # FA
        DTmeasures2std.connect(dti, 'FA',
                               flt_fa, 'in_file')
        # MD
        DTmeasures2std.connect(dti, 'MD',
                               flt_md, 'in_file')
        DTmeasures2std.connect(flt_fa, 'out_matrix_file',
                               flt_md, 'apply_xfm')
        # MO
        DTmeasures2std.connect(dti, 'MO',
                               flt_mo, 'in_file')
        DTmeasures2std.connect(flt_fa, 'out_matrix_file',
                               flt_mo, 'apply_xfm')
        # L! - Axial Diff
        DTmeasures2std.connect(dti, 'L1',
                               flt_l1, 'in_file')
        DTmeasures2std.connect(flt_fa, 'out_matrix_file',
                               flt_l1, 'apply_xfm')
        # Rad diff
        DTmeasures2std.connect(calc_radial, 'out_file',
                               flt_rad, 'in_file')
        DTmeasures2std.connect(flt_fa, 'out_matrix_file',
                               flt_rad, 'apply_xfm')

        # Running the workflow
        DTmeasures2std.base_dir = os.path.abspath(out_directory)
        DTmeasures2std.run('MultiProc', plugin_args={'n_procs': 8})


def main():
    from os.path import join as opj
    from bids.grabbids import BIDSLayout

    CWD = '/home/asier/git/surface-kljajevic-17'
    base_directory = opj(CWD, 'data')
    out_directory = opj(CWD, 'data/processed')
    layout = BIDSLayout(base_directory)

    subjects = layout.get_subjects()
    subject_list = ["sub-" + subject for subject in subjects]

    os.chdir(out_directory)
    DTmeasures2std(subject_list, base_directory, out_directory)


if __name__ == '__main__':
    # main should return 0 for success, something else (usually 1) for error.
    sys.exit(main())
