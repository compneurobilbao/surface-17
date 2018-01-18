#! /usr/bin/env python
import os
import sys


def FA_2_std(subject_list, base_directory, out_directory):

    # ==================================================================
    # Loading required packages
    import nipype.pipeline.engine as pe
    import nipype.interfaces.utility as util
    import nipype.interfaces.fsl as fsl

    from nipype import SelectFiles
    import os

    # ==================================================================
    # Defining the nodes for the workflow

    # Getting the subject ID
    infosource = pe.Node(interface=util.IdentityInterface(
        fields=['subject_id']), name='infosource')
    infosource.iterables = ('subject_id', subject_list)

    # Getting the relevant diffusion-weighted data
    templates = dict(fa='_subject_id_{subject_id}/dti/dtifit__FA.nii.gz')

    selectfiles = pe.Node(SelectFiles(templates),
                          name='selectfiles')
    selectfiles.inputs.base_directory = os.path.abspath(base_directory)

    # FA to Standard
    flt_fa = pe.Node(interface=fsl.FLIRT(dof=12,
                                         cost_func='mutualinfo',
                                         reference ='/usr/share/fsl/5.0/data/standard/MNI152_T1_1mm_brain.nii.gz'),
                     name='flt_fa')

    # ==================================================================
    # Setting up the workflow
    fa_connectome = pe.Workflow(name='FA_connectome_qc')

    # Reading in files
    fa_connectome.connect(infosource, 'subject_id', selectfiles, 'subject_id')

    # Denoising
    fa_connectome.connect(selectfiles, 'fa', flt_fa, 'in_file')

    # Running the workflow
    fa_connectome.base_dir = os.path.abspath(out_directory)
#        fa_connectome.write_graph()
    fa_connectome.run('MultiProc', plugin_args={'n_procs': 8})


def main():
    from os.path import join as opj
#    from bids.grabbids import BIDSLayout

    CWD = '/home/asier/git/surface-kljajevic-17'
#    base_directory = opj(CWD, 'data/raw/bids')
    out_directory = opj(CWD, 'data/processed_qc')
#    layout = BIDSLayout(base_directory)
    input_directory = opj(CWD, 'data/processed_qc/FA_connectome_qc/')
    subjects_file = '/home/asier/git/surface-kljajevic-17/src/fa/correct_qa/bad_scans.txt'

    with open(subjects_file, "r") as ins:
        subjects = []
        for line in ins:
            subjects.append(line)
    subjects = [subjects.rstrip('\n') for subjects in subjects]
    subject_list = ["sub-" + str(subject) for subject in subjects]
    os.chdir(out_directory)
    FA_2_std(subject_list, input_directory, out_directory)


if __name__ == '__main__':
    # main should return 0 for success, something else (usually 1) for error.
    sys.exit(main())
