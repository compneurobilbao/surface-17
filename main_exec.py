#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 12:47:19 2017

@author: asier
"""
from multiprocessing import Pool
from multiprocessing import Process, JoinableQueue

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
    
    for subject in subjects:
        print(subject)
        try:
            main_workflow(subject)
        except:
            with open("error_report.txt", "a") as fout:
                fout.write("error in {} \n".format(subject))
