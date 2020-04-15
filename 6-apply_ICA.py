#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 02:03:39 2020

@author: wexu
"""
import mne
import numpy as np
from config_SYN_Human import study_path,EEG_data_path,exp
import os
from mne.preprocessing import read_ica

for ID in exp.index:
    
    fname=os.path.join(study_path,ID+'.edf')
    
    ica=read_ica(fname.replace(".edf", "-ica.fif"))
    epochs=mne.read_epochs(fname.replace(".edf", "_cleaned-epo.fif"))
    ica.exclude = np.load(fname.replace(".edf",'ICA_excludes.npy')).tolist()
    
    ica.apply(epochs,exclude=ica.exclude)
    
    epochs.plot(n_channels=66,n_epochs=25,scalings=dict(eeg=200e-6),block=True)
    epochs.drop_bad()
    
    epochs.save(fname.replace(".edf", "_ICA_cleaned-epo.fif"),overwrite=False)
