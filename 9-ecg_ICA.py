#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 17:36:10 2020

@author: wexu
"""

import mne
from config_SYN_Human import study_path,exp
import os
import json
import numpy as np
from mne.preprocessing import read_ica


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



    event_id = 999
    ecg_events, ch_ecg, average_pulse = mne.preprocessing.find_ecg_events(raw, event_id,ch_name='EKG')    
        
    CS_epochs=mne.read_epochs(os.path.join(study_path,ID+"_ICA_cleaned-epo.fif"))
    
    ecg_bCS_events=[]
    
    for CS_event in CS_epochs.events:
        
        ecg_event=ecg_events[np.where(CS_event[0] > ecg_events[:,0])][-1]
        
        if (CS_event[0]-ecg_event[0]) <1000:
          ecg_bCS_events.append(ecg_event) 
    
    ecg_bCS_events=np.array(ecg_bCS_events)
    
    ecg_epochs = mne.Epochs(raw, events=ecg_bCS_events, event_id=event_id, tmin=-0.2, tmax=1, baseline=None)
    ecg_epochs.save(fname.replace(".edf", "-ecg_epo.fif"),overwrite=True)
    
    # ecg_epochs = mne.preprocessing.create_ecg_epochs(raw,ch_name='EKG')
    # ecg_epochs.plot(['EKG']) 
    
for ID in exp.index:
    
    fname=os.path.join(study_path,ID+'.edf')
    
    ica=read_ica(fname.replace(".edf", "-ica.fif"))
    epochs=mne.read_epochs(fname.replace(".edf", "-ecg_epo.fif"))
    ica.exclude = np.load(fname.replace(".edf",'ICA_excludes.npy')).tolist()
    
    ica.apply(epochs,exclude=ica.exclude)
    
    epochs.save(fname.replace(".edf", "_ICA_cleaned-ecg_epo.fif"),overwrite=False)

xxx
 
ES_ID=exp[exp['group']=='ES'].index
ED_ID=exp[exp['group']=='ED'].index
IS_ID=exp[exp['group']=='IS'].index
ID_ID=exp[exp['group']=='ID'].index
     
GA_ECG_S= mne.grand_average([mne.read_epochs(os.path.join(study_path,ID+"-ecg_epo.fif")).average().apply_baseline((None)) for ID in ES_ID.append(IS_ID)])
GA_ECG_S.comment='without_ICA_S'

GA_ECG_D= mne.grand_average([mne.read_epochs(os.path.join(study_path,ID+"-ecg_epo.fif")).average().apply_baseline((None)) for ID in ED_ID.append(ID_ID)])
GA_ECG_D.comment='without_ICA_D'

GA_ECG_ICA_S= mne.grand_average([mne.read_epochs(os.path.join(study_path,ID+"_ICA_cleaned-ecg_epo.fif")).average().apply_baseline((None)) for ID in ES_ID.append(IS_ID)])
GA_ECG_ICA_S.comment='with_ICA_S'

GA_ECG_ICA_D= mne.grand_average([mne.read_epochs(os.path.join(study_path,ID+"_ICA_cleaned-ecg_epo.fif")).average().apply_baseline((None)) for ID in ED_ID.append(ID_ID)])
GA_ECG_ICA_D.comment='with_ICA_D'


mne.viz.plot_evoked_topo([GA_ECG_S,GA_ECG_ICA_S])
mne.viz.plot_evoked_topo([GA_ECG_D,GA_ECG_ICA_D])

mne.viz.plot_evoked_topo([GA_ECG_S,GA_ECG_ICA_S,GA_ECG_D,GA_ECG_ICA_D])
