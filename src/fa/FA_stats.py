#! /usr/bin/env python
import os
import sys


def get_measure(file, mask, measure):


    return result

def FAstats(subject_list, base_directory, out_directory):

###############################################################################################
###calculate statistics on an image (mean, no indluding voxels with zeros) and store as variable
###############################################################################################
#mean_nozeros=`fslstats 'image_1.nii.gz' -M` ##mean, not including voxels with zeros
#mean_zeros=`fslstats 'image_1.nii.gz' -m` ##mean, including voxels with zeros
#sd_nozeros=`fslstats 'image_1.nii.gz' -S` ##standard deviation, not including voxels with zeros
#sd_zeros=`fslstats 'image_1.nii.gz' -s` ##standard deviation, including voxels with zeros
#
###############################################################################################
###apply a mask to an image
###############################################################################################
#fslmaths 'image_1.nii.gz' -mas 'mask.nii.gz' 'output_image.nii.gz'        

    measures = ['-s', '-m']
    masks = []
    modalities = ['fa', 'md', 'mo', 'l1', 'radial']

    for subject in subject_list:
        for modality in modalities:
            # get input files
            for mask in masks:
                for measure in measures:
                    
                    result = get_measure(file, mask, measure)

                    # save append subject, modality, mask_type and measure

    
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
    FAstats(subject_list, base_directory, out_directory)


if __name__ == '__main__':
    # main should return 0 for success, something else (usually 1) for error.
    sys.exit(main())
