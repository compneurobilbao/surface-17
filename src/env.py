# -*- coding: utf-8 -*-
import os
from os.path import join as opj

cwd = os.getcwd()

DATA = opj(cwd, 'data')
RAW_DATA = opj(DATA, 'raw')
BIDS_DATA = opj(RAW_DATA, 'bids')
SESSION_TYPES = ['ses-001']
ATLAS_TYPES = ['atlas_2514']
HEUDICONV_BIN = '/home/asier/git/ruber/src/heudiconv/heudiconv'
HEUDICONV_FOLDER = '/home/asier/git/ruber/src/heudiconv'

NEIGHBOURS = [0, 1]
# TODO: this as iterable variable and convert pipeline to nipype
ELECTRODE_SPHERE_SIZE = [2]
