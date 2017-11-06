#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 12:35:55 2017

@author: asier
"""
import os
import sys


def FA2std(subject_list, base_directory, out_directory):

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
        templates = dict(fa='_subject_id_{subject_id}/tensor2metric/fa.nii.gz')

        selectfiles = pe.Node(SelectFiles(templates),
                              name='selectfiles')
        selectfiles.inputs.base_directory = os.path.abspath(base_directory)

        # FA to Standard
        flt = pe.Node(
                interface=fsl.FLIRT(dof=12,
                                    cost_func='mutualinfo',
                                    reference ='/usr/share/fsl/5.0/data/standard/MNI152_T1_1mm_brain.nii.gz'),
                                    name='flt')

        # ==================================================================
        # Setting up the workflow
        FA2std = pe.Workflow(name='FA2std')

        # Reading in files
        FA2std.connect(infosource, 'subject_id',
                              selectfiles, 'subject_id')

        # Denoising
        FA2std.connect(selectfiles, 'fa',
                              flt, 'in_file')

        # Running the workflow
        FA2std.base_dir = os.path.abspath(out_directory)
        FA2std.run('MultiProc', plugin_args={'n_procs': 8})


def main():
    from os.path import join as opj
    from bids.grabbids import BIDSLayout

    CWD = '/home/asier/git/surface-kljajevic-17'
    base_directory = opj(CWD, 'data/processed/FA_connectome')
    out_directory = opj(CWD, 'data/processed')
    layout = BIDSLayout(base_directory)

    subjects = layout.get_subjects()
    subject_list = ["sub-" + subject for subject in subjects]

    os.chdir(out_directory)
    FA2std(subject_list, base_directory, out_directory)


if __name__ == '__main__':
    # main should return 0 for success, something else (usually 1) for error.
    sys.exit(main())
