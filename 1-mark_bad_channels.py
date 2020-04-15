#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 23:13:02 2020

@author: wexu
"""

import mne
from config_SYN_Human import study_path,exp
import os
import json

for ID in exp.index[29:30]:
    
    fname=os.path.join(study_path,ID+'.edf')
    multiple=['_1','_2'] if exp.loc[ID,'multiple']==1 else ['']
    
    input_fnames=[os.path.join(study_path,ID+mul+'.edf') for mul in multiple]
      
    raws = [mne.io.read_raw_edf(input_fname=input_fname,
                              misc=['CS','US','Respiration','EKG','EMG','EDA'],
                              preload=True) for input_fname in input_fnames ]
    if len(raws)>1:
        raw=mne.concatenate_raws(raws)
    else:
        raw=raws[0]
    
    montage = mne.channels.read_custom_montage(fname='/nashome1/wexu/Scripts/MNE_Scripts/SynchronyHuman/GSN-HydroCel-129.bvef')
    raw.set_montage(montage)
    
    raw.filter(0.5,30)
    
    raw.set_eeg_reference('average',projection=False)
    
    if os.path.isfile(fname.replace('.edf', "-bads.txt")):    
        with open(fname.replace('.edf', "-bads.txt"), 'r') as filehandle:
            raw.info['bads']=json.load(filehandle)
    
    if os.path.isfile(fname.replace('.edf', "-annot.fif")):
        raw.set_annotations(mne.read_annotations(fname.replace('.edf', "-annot.fif")))
    
    raw.pick(['eeg']).plot(n_channels=65,duration=40.0,
                           scalings=dict(eeg=100e-6),block=True)
    
    if raw.info['bads']:
        with open(fname.replace('.edf', "-bads.txt"), 'w') as filehandle:
            json.dump(raw.info['bads'], filehandle)
        
    if raw.annotations:
        raw.annotations.save(fname.replace('.edf', "-annot.fif"))
        