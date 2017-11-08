#! /usr/bin/env python
import os
import sys

from nipype.interfaces.base import BaseInterface
from nipype.interfaces.base import BaseInterfaceInputSpec
from nipype.interfaces.base import File
from nipype.interfaces.base import TraitedSpec

# ==================================================================
"""
Denoising with non-local means
This function is based on the example in the Dipy preprocessing tutorial:
http://nipy.org/dipy/examples_built/denoise_nlmeans.html#example-denoise-nlmeans
"""


class DipyDenoiseInputSpec(BaseInterfaceInputSpec):
    in_file = File(exists=True, desc='diffusion weighted volume for denoising',
                   mandatory=True)


class DipyDenoiseOutputSpec(TraitedSpec):
    out_file = File(exists=True, desc="denoised diffusion-weighted volume")


class DipyDenoise(BaseInterface):
    input_spec = DipyDenoiseInputSpec
    output_spec = DipyDenoiseOutputSpec

    def _run_interface(self, runtime):
        import nibabel as nib
        import numpy as np
        from dipy.denoise.nlmeans import nlmeans
        from nipype.utils.filemanip import split_filename

        fname = self.inputs.in_file
        img = nib.load(fname)
        data = img.get_data()
        affine = img.get_affine()
        mask = data[..., 0] > 80
        a = data.shape

        denoised_data = np.ndarray(shape=data.shape)
        for image in range(0, a[3]):
            print(str(image + 1) + '/' + str(a[3] + 1))
            dat = data[..., image]
            # Calculating the standard deviation of the noise
            sigma = np.std(dat[~mask])
            den = nlmeans(dat, sigma=sigma, mask=mask)
            denoised_data[:, :, :, image] = den

        _, base, _ = split_filename(fname)
        nib.save(nib.Nifti1Image(denoised_data, affine),
                 base + '_denoised.nii')

        return runtime

    def _list_outputs(self):
        from nipype.utils.filemanip import split_filename
        import os
        outputs = self._outputs().get()
        fname = self.inputs.in_file
        _, base, _ = split_filename(fname)
        outputs["out_file"] = os.path.abspath(base + '_denoised.nii')
        return outputs

# ======================================================================
# Extract b0


class Extractb0InputSpec(BaseInterfaceInputSpec):
    in_file = File(
        exists=True, desc='diffusion-weighted image (4D)', mandatory=True)


class Extractb0OutputSpec(TraitedSpec):
    out_file = File(exists=True, desc="First volume of the dwi file")


class Extractb0(BaseInterface):
    input_spec = Extractb0InputSpec
    output_spec = Extractb0OutputSpec

    def _run_interface(self, runtime):
        import nibabel as nib
        img = nib.load(self.inputs.in_file)
        data = img.get_data()
        affine = img.get_affine()

        from nipype.utils.filemanip import split_filename
        import os
        outputs = self._outputs().get()
        fname = self.inputs.in_file
        _, base, _ = split_filename(fname)
        nib.save(nib.Nifti1Image(data[..., 0], affine),
                 os.path.abspath(base + '_b0.nii.gz'))
        return runtime

    def _list_outputs(self):
        from nipype.utils.filemanip import split_filename
        import os
        outputs = self._outputs().get()
        fname = self.inputs.in_file
        _, base, _ = split_filename(fname)
        outputs["out_file"] = os.path.abspath(base + '_b0.nii.gz')
        return outputs


def FA_connectome(subject_list, base_directory, out_directory):

    # ==================================================================
    # Loading required packages
    import nipype.pipeline.engine as pe
    import nipype.interfaces.utility as util
    import nipype.interfaces.fsl as fsl
    import nipype.interfaces.dipy as dipy
    from FA_Connectome import Extractb0 as extract_b0
    import nipype.algorithms.misc as misc

    from nipype import SelectFiles
    import os

    # ==================================================================
    # Defining the nodes for the workflow

    # Utility nodes
    gunzip = pe.Node(interface=misc.Gunzip(), name='gunzip')

    # Getting the subject ID
    infosource = pe.Node(interface=util.IdentityInterface(
        fields=['subject_id']), name='infosource')
    infosource.iterables = ('subject_id', subject_list)

    # Getting the relevant diffusion-weighted data
    templates = dict(dwi='{subject_id}/dwi/{subject_id}_dwi.nii.gz',
                     bvec='{subject_id}/dwi/{subject_id}_dwi.bvec',
                     bval='{subject_id}/dwi/{subject_id}_dwi.bval')

    selectfiles = pe.Node(SelectFiles(templates),
                          name='selectfiles')
    selectfiles.inputs.base_directory = os.path.abspath(base_directory)

    # Denoising
    denoise = pe.Node(interface=DipyDenoise(), name='denoise')

    # Eddy-current and motion correction
    eddycorrect = pe.Node(interface=fsl.epi.EddyCorrect(), name='eddycorrect')
    eddycorrect.inputs.ref_num = 0

    # Upsampling
    resample = pe.Node(interface=dipy.Resample(
        interp=3, vox_size=(1., 1., 1.)), name='resample')

    # Extract b0 image
    extract_b0 = pe.Node(interface=extract_b0(), name='extract_b0')

    # Create a brain mask
    bet = pe.Node(interface=fsl.BET(
        frac=0.3, robust=False, mask=True), name='bet')

    dti = pe.Node(interface=fsl.DTIFit(),
                  name='dti')
    calc_radial = pe.Node(interface=fsl.MultiImageMaths(op_string='-add %s -div 2',
                                                        out_file='radial_diff.nii.gz'),
                          name='calc_radial')
    # FA to Standard
    flt_fa = pe.Node(interface=fsl.FLIRT(dof=12,
                                         cost_func='mutualinfo',
                                         reference ='/usr/share/fsl/5.0/data/standard/MNI152_T1_1mm_brain.nii.gz'),
                     name='flt_fa')

    flt_md = pe.Node(interface=fsl.FLIRT(dof=12,
                                         cost_func='mutualinfo',
                                         reference='/usr/share/fsl/5.0/data/standard/MNI152_T1_1mm_brain.nii.gz',
                                         apply_xfm=True),
                     name='flt_md')

    flt_mo = pe.Node(interface=fsl.FLIRT(dof=12,
                                         cost_func='mutualinfo',
                                         reference='/usr/share/fsl/5.0/data/standard/MNI152_T1_1mm_brain.nii.gz',
                                         apply_xfm=True),
                     name='flt_mo')

    flt_l1 = pe.Node(interface=fsl.FLIRT(dof=12,
                                         cost_func='mutualinfo',
                                         reference='/usr/share/fsl/5.0/data/standard/MNI152_T1_1mm_brain.nii.gz',
                                         apply_xfm=True),
                     name='flt_l1')

    flt_rad = pe.Node(interface=fsl.FLIRT(dof=12,
                                          cost_func='mutualinfo',
                                          reference='/usr/share/fsl/5.0/data/standard/MNI152_T1_1mm_brain.nii.gz',
                                          apply_xfm=True),
                      name='flt_rad')


    # ==================================================================
    # Setting up the workflow
    fa_connectome = pe.Workflow(name='FA_connectome')

    # Reading in files
    fa_connectome.connect(infosource, 'subject_id', selectfiles, 'subject_id')

    # Denoising
    fa_connectome.connect(selectfiles, 'dwi', denoise, 'in_file')

    # Eddy current and motion correction
    fa_connectome.connect(denoise, 'out_file', eddycorrect, 'in_file')
    fa_connectome.connect(eddycorrect, 'eddy_corrected', resample, 'in_file')
    fa_connectome.connect(resample, 'out_file', extract_b0, 'in_file')
    fa_connectome.connect(resample, 'out_file', gunzip, 'in_file')

    # Brain extraction
    fa_connectome.connect(extract_b0, 'out_file', bet, 'in_file')

    # ==================================================================
    # Reading in files
    fa_connectome.connect(infosource, 'subject_id',
                           selectfiles, 'subject_id')

    # Calc measures
    fa_connectome.connect(selectfiles, 'dwi',
                           dti, 'dwi')
    fa_connectome.connect(selectfiles, 'bvecs',
                           dti, 'bvecs')
    fa_connectome.connect(selectfiles, 'bvals',
                           dti, 'bvals')
    fa_connectome.connect(selectfiles, 'mask',
                           dti, 'mask')
    # Calc radial diff
    fa_connectome.connect(dti, 'L2',
                           calc_radial, 'in_file')
    fa_connectome.connect(dti, 'L3',
                           calc_radial, 'operand_files')

    # FA
    fa_connectome.connect(dti, 'FA',
                           flt_fa, 'in_file')
    # MD
    fa_connectome.connect(dti, 'MD',
                           flt_md, 'in_file')
    fa_connectome.connect(flt_fa, 'out_matrix_file',
                           flt_md, 'in_matrix_file')
    # MO
    fa_connectome.connect(dti, 'MO',
                           flt_mo, 'in_file')
    fa_connectome.connect(flt_fa, 'out_matrix_file',
                           flt_mo, 'in_matrix_file')
    # L! - Axial Diff
    fa_connectome.connect(dti, 'L1',
                           flt_l1, 'in_file')
    fa_connectome.connect(flt_fa, 'out_matrix_file',
                           flt_l1, 'in_matrix_file')
    # Rad diff
    fa_connectome.connect(calc_radial, 'out_file',
                           flt_rad, 'in_file')
    fa_connectome.connect(flt_fa, 'out_matrix_file',
                           flt_rad, 'in_matrix_file')


    # Running the workflow
    fa_connectome.base_dir = os.path.abspath(out_directory)
#        fa_connectome.write_graph()
    fa_connectome.run('MultiProc', plugin_args={'n_procs': 8})
        

def main():
    from os.path import join as opj
    from bids.grabbids import BIDSLayout
    
    CWD = '/home/asier/git/surface-kljajevic-17'
    base_directory = opj(CWD,'data/raw/bids')
    out_directory = opj(CWD,'data/processed')
    layout = BIDSLayout(base_directory)

    subjects = layout.get_subjects()
    subject_list = ["sub-" + subject for subject in subjects]

    os.chdir(out_directory)
    FA_connectome(subject_list, base_directory, out_directory)


if __name__ == '__main__':
    # main should return 0 for success, something else (usually 1) for error.
    sys.exit(main())
