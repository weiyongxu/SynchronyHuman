#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 00:29:26 2020

@author: wexu
"""

import mne
from config_SYN_Human import study_path,exp
import os

for ID in exp.index[29:]:

    fname=os.path.join(study_path,ID+'.edf') 
    
    epochs=mne.read_epochs(fname.replace(".edf", "-epo.fif"))
    
    epochs.plot(n_channels=128,n_epochs=30,scalings=dict(eeg=250e-6),block=True)
    
    epochs.drop_bad()
    
    epochs.save(fname.replace(".edf", "_cleaned-epo.fif"),overwrite=True)


