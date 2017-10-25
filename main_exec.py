#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 12:47:19 2017

@author: asier
"""
from multiprocessing import Pool
import os
from os.path import join as opj
from bids.grabbids import BIDSLayout

from src.atlas_wf import main_workflow


if __name__ == "__main__":
    
    
    cwd = os.getcwd()
    bids_path = opj(cwd, 'data', 'raw', 'bids')
    layout = BIDSLayout(bids_path)
    
    subjects = layout.get_subjects()
    subjects = ["sub-" + subject for subject in subjects]
    
    args = [tuple([sub])
            for sub in subjects[0:1]]

    pool = Pool()
    pool.map(main_workflow, args)
    pool.close()