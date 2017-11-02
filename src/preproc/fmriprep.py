#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 11:35:55 2017

@author: asier
"""
from src.env import BIDS_DATA, DATA
from os.path import join as opj
from src.postproc.utils import execute

DATA_DIR = BIDS_DATA
OUTPUT_DIR = opj(DATA, 'processed')
WORK_DIR = opj(DATA, 'interim')


def run_fmriprep(sub):

    command = [
               'docker', 'run', '-i', '--rm',
               '-v', DATA_DIR + ':/data:ro',
               '-v', OUTPUT_DIR + ':/output',
               '-v', WORK_DIR + ':/work',
               '-w', '/work',
               'poldracklab/fmriprep:latest',
               '/data', '/output', 'participant',
               '--participant_label', sub,
               '-w', '/work', '--no-freesurfer', '--ignore', 'fieldmaps',
               '--output-space', 'template',
               '--template', 'MNI152NLin2009cAsym',
            ]

    for output in execute(command):
        print(output)


def run_mriqc(sub):

    command = [
           'docker', 'run', '-i', '--rm',
           '-v', DATA_DIR + ':/data:ro',
           '-v', OUTPUT_DIR + ':/output',
           '-v', WORK_DIR + ':/work',
           '-w', '/work',
           'poldracklab/mriqc:latest',
           '/data', '/output', 'participant',
           '--participant_label', sub,
           '-w', '/work', '--verbose-reports',
        ]

    for output in execute(command):
        print(output)


# sudo chmod 777 -R $DATA


#def run_fmriprep(sub):
#
#    command = [
#           'singularity', 'run', opj(os.getcwd(), 'fmriprep-sing.img',
#                                     'poldracklab_fmriprep_latest-2017-08-12-9147b730c142.img'),
#           DATA_DIR,
#           OUTPUT_DIR,
#           'participant',
#           '--participant_label', sub,
#           '-w', WORK_DIR, '--no-freesurfer', '--ignore', 'fieldmaps',
#           '--output-space', 'template',
#           '--template', 'MNI152NLin2009cAsym',
#        ]
#    for output in execute(command):
#        print(output)
