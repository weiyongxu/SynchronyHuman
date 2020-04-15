#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 01:35:05 2020

@author: wexu
"""

import mne
from config_SYN_Human import study_path,EEG_data_path,exp
import os
import json
from mne.preprocessing import ICA

for ID in exp.index:

    fname=os.path.join(study_path,ID+'.edf') 
    
    epochs=mne.read_epochs(fname.replace(".edf", "_cleaned-epo.fif"))
    
    ica = ICA(method='fastica',n_components=0.99,max_iter=1000)
    ica.fit(epochs)
    ica.save(fname.replace(".edf", "-ica.fif"))