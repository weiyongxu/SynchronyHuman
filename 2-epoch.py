#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 22:12:21 2020

@author: wexu
"""

import mne
from config_SYN_Human import study_path,exp
import os
import json

for ID in exp.index:

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
    
    events=mne.events_from_annotations(raw)
    event_id={'CS': events[1]['8Bit 1']+10} #,'US': events[1]['8Bit 2']+10
    events=events[0]
    for i in range(len(events)-1):
        if events[i,2]==1 and events[i+1,2]==2 and (events[i+1,0]-events[i,0])<1000:
            events[i,2]=events[i,2]+10
            events[i+1,2]=events[i+1,2]+10
    
    if os.path.isfile(fname.replace('.edf', "-bads.txt")):    
        with open(fname.replace('.edf', "-bads.txt"), 'r') as filehandle:
            raw.info['bads']=json.load(filehandle)
    if os.path.isfile(fname.replace('.edf', "-annot.fif")):
        raw.set_annotations(mne.read_annotations(fname.replace('.edf', "-annot.fif")))
    
    raw.interpolate_bads()
    
    raw.filter(0.5,30)
    
    raw.set_eeg_reference('average',projection=False)
          
    epochs = mne.Epochs(raw, events=events, event_id=event_id, tmin=-0.1, tmax=0.5, baseline=None)
    epochs.save(fname.replace(".edf", "-epo.fif"),overwrite=True)
    
