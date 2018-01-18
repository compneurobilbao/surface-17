# -*- coding: utf-8 -*-

import os
from os.path import join as opj
import nibabel as nib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


CWD = '/home/asier/git/surface-kljajevic-17'
base_directory = opj(CWD, 'data/raw/bids')
input_directory = opj(CWD, 'data/processed_qc/FA_connectome_qc')
out_directory = opj(CWD, 'data/output_for_vanja_qc')
subjects_file = '/home/asier/git/surface-kljajevic-17/src/fa/correct_qa/bad_scans.txt'

with open(subjects_file, "r") as ins:
    subjects = []
    for line in ins:
        subjects.append(line)
subjects = [subjects.rstrip('\n') for subjects in subjects]
subject_list = ["sub-" + str(subject) for subject in subjects]


def multipage(filename, figs=None, dpi=200):
    pp = PdfPages(filename)
    if figs is None:
        figs = [plt.figure(n) for n in plt.get_fignums()]
    for fig in figs:
        fig.savefig(pp, format='pdf')
    pp.close()


def show_slices(slices):
    """ Function to display row of image slices """
    fig, axes = plt.subplots(1, len(slices))
    for i, slice in enumerate(slices):
        axes[i].imshow(slice.T, cmap="gray", origin="lower")

    return fig


def QC_plots():
    for acq_type in os.listdir(out_directory):
        print(acq_type)
        acp_path = opj(out_directory, acq_type)

        figures = []

        for sub_acq in os.listdir(acp_path):
            file_path = opj(acp_path, sub_acq)
            epi_img_data = nib.load(file_path).get_data()
            slice_0 = epi_img_data[91, :, :]
            slice_1 = epi_img_data[:, 109, :]
            slice_2 = epi_img_data[:, :, 91]
            show_slices([slice_0, slice_1, slice_2])
            ax = plt.title('Subject_' + sub_acq)
            fig = ax.get_figure()
            figures.append(fig)
            plt.close()

        multipage(opj(out_directory,
                      'QC_' + acq_type + '.pdf'),
                  figures,
                  dpi=250)
