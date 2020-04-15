#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 01:58:13 2020

@author: wexu
"""
import mne
import numpy as np
from config_SYN_Human import study_path,exp
import os
from mne.preprocessing import read_ica

for ID in exp.index:

    fname=os.path.join(study_path,ID+'.edf') 
    
    ica=read_ica(fname.replace(".edf", "-ica.fif"))
    epochs=mne.read_epochs(fname.replace(".edf", "_cleaned-epo.fif"))
    
    ica.plot_sources(epochs,block = True)   

    print(ica.exclude)        
    ica.plot_components(inst=epochs)
    
    print(ica.exclude)
    ica.plot_sources(epochs,block = True)
    
    np.save(fname.replace(".edf",'ICA_excludes.npy'),ica.exclude)