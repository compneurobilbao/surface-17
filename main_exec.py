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


# the function for each process in our pool
def pool_func(q):
    while True:
        allRenderArg, otherArg = q.get() # blocks until the queue has an item
        try:
            render(allRenderArg, otherArg)
        finally: q.task_done()
        
        

if __name__ == "__main__":
    
    
    cwd = os.getcwd()
    bids_path = opj(cwd, 'data', 'raw', 'bids')
    layout = BIDSLayout(bids_path)
    
    subjects = layout.get_subjects()
    subjects = ["sub-" + subject for subject in subjects]
    
    args = [tuple([sub])
            for sub in subjects]





# best practice to go through main for multiprocessing
    # create the pool
    pool_size = 8
    pool = []
    q = JoinableQueue()
    for x in range(pool_size):
        pool.append(Process(target=main_exec, args))

    # start the pool, making it "daemonic" (the pool should exit when this proc exits)
    for p in pool:
        p.daemon = True
        p.start()

    # submit jobs to the queue
    for i in range(totalInstances):
        q.put((allRenderArgs[i], args[2]))

    # wait for all tasks to complete, then exit
    q.join()
    pool = Pool()
    pool.map(main_workflow, args)
    pool.close()