#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 21:25:57 2020

@author: wexu
"""

import mne
from config_SYN_Human import study_path,exp
import os

# Grand avg for all groups      
GA= mne.grand_average([mne.read_epochs(os.path.join(study_path,ID+"_ICA_cleaned-epo.fif")).average().apply_baseline((None,0)) for ID in exp.index])
GA.plot_joint()
#GA.plot_sensors(show_names=False,kind='select') #Channel 6,7,106 ROI

groups=['ES','ED','IS','ID']
groups_full=['Exhale Systole','Exhale Diastole','Inhale Systole','Inhale Diastole']

GAs=dict()
for group,group_full in zip(groups,groups_full):    
    GAs[group_full]= mne.grand_average([mne.read_epochs(os.path.join(study_path,ID+"_ICA_cleaned-epo.fif")).average().apply_baseline((None,0)) 
                            for ID in exp[exp['group']==group].index])
    GAs[group_full].comment=group_full

mne.viz.plot_compare_evokeds(GAs,combine='mean',
                             picks=['6','7','106'],
                             show_sensors=True,
                             colors=['#377eb8', '#ff7f00', '#4daf4a','#984ea3']
                                     )

# https://gist.github.com/thriveth/8560036
# ['#377eb8', '#ff7f00', '#4daf4a',
#  '#f781bf', '#a65628', '#984ea3',
#  '#999999', '#e41a1c', '#dede00']

for evk in list(GAs.values()):
    evk.plot_topomap(times=[0.117,0.188],vmin=-14,vmax=14,average=0.01,
                     title=evk.comment).savefig(evk.comment+'.pdf')
    
N1_lat=dict()
P2_lat=dict()
N1_amp=dict()
P2_amp=dict()

ROI_chs=['6','7','106']
for ID in exp.index:
    evk=mne.read_epochs(os.path.join(study_path,ID+"_ICA_cleaned-epo.fif")).average().apply_baseline((None,0)).pick_channels(ROI_chs)
    _,N1_lat[ID]=evk.get_peak(tmin=0.09,tmax=0.15,mode='neg')
    _,P2_lat[ID]=evk.get_peak(tmin=0.16,tmax=0.22,mode='pos')    
    N1_amp[ID]=evk.copy().crop(N1_lat[ID]-0.005,N1_lat[ID]+0.005).to_data_frame().loc[:,ROI_chs].mean().mean()
    P2_amp[ID]=evk.copy().crop(P2_lat[ID]-0.005,P2_lat[ID]+0.005).to_data_frame().loc[:,ROI_chs].mean().mean()
    
import pandas as pd
df=pd.DataFrame(columns=['group','N1 amplitude','P2 amplitude','N1 latency','P2 latency','resp','ecg'])
    
for group,group_full in zip(groups,groups_full):    
    for ID in exp[exp['group']==group].index:
        df.loc[ID]=[group_full,N1_amp[ID],P2_amp[ID],N1_lat[ID],P2_lat[ID],group[0],group[1]]

df.to_csv('N1P2.csv')

import seaborn
import matplotlib.pyplot as plt
f, axes = plt.subplots(2, 2,sharex=True)

for y, pos in zip(['N1 amplitude','P2 amplitude','N1 latency','P2 latency'],[[0,0],[0,1],[1,0],[1,1]]):
    seaborn.boxplot(x='group',y=y, data=df,ax=axes[pos[0],pos[1]],
                    palette=['#377eb8', '#ff7f00', '#4daf4a','#984ea3'])    
    seaborn.swarmplot(x='group',y=y, data=df,color=".3", alpha=0.6, ax=axes[pos[0],pos[1]])
plt.tight_layout()
    
# main effects

groups2=[['ES','ED'],['IS','ID'],['ED','ID'],['ES','IS']]
groups_full2=['Exhale','Inhale','Diastole','Systole']

GA_main=dict()


for group,group_full in zip(groups2,groups_full2): 
    IDs=exp[exp['group']==group[0]].index.append(exp[exp['group']==group[1]].index)
    GA_main[group_full]= mne.grand_average([mne.read_epochs(os.path.join(study_path,ID+"_ICA_cleaned-epo.fif")).average().apply_baseline((None,0)) 
                            for ID in IDs])
    GA_main[group_full].comment=group_full

for evk in list(GA_main.values()):
    evk.plot_topomap(times=[0.117,0.188],vmin=-14,vmax=14,average=0.01,
                     title=evk.comment).savefig(evk.comment+'.pdf')

mne.viz.plot_compare_evokeds(dict(list(GA_main.items())[0:2]),combine='mean',
                             picks=['6','7','106'],
                             show_sensors=True,
                             colors=['#377eb8', '#ff7f00', '#4daf4a','#984ea3']
                                     )        
    
mne.viz.plot_compare_evokeds(dict(list(GA_main.items())[2:5]),combine='mean',
                             picks=['6','7','106'],
                             show_sensors=True,
                             colors=['#377eb8', '#ff7f00', '#4daf4a','#984ea3']
                                     )  

f, axes = plt.subplots(2, 2,sharex=True)
for y, pos in zip(['N1 amplitude','P2 amplitude','N1 latency','P2 latency'],[[0,0],[0,1],[1,0],[1,1]]):
    seaborn.boxplot(x='resp',y=y, data=df,ax=axes[pos[0],pos[1]],
                    palette=['#377eb8', '#ff7f00', '#4daf4a','#984ea3'])    
    seaborn.swarmplot(x='resp',y=y, data=df,color=".3", alpha=0.6, ax=axes[pos[0],pos[1]])
plt.tight_layout()

f, axes = plt.subplots(2, 2,sharex=True)
for y, pos in zip(['N1 amplitude','P2 amplitude','N1 latency','P2 latency'],[[0,0],[0,1],[1,0],[1,1]]):
    seaborn.boxplot(x='ecg',y=y, data=df,ax=axes[pos[0],pos[1]],
                    palette=['#377eb8', '#ff7f00', '#4daf4a','#984ea3'])    
    seaborn.swarmplot(x='ecg',y=y, data=df,color=".3", alpha=0.6, ax=axes[pos[0],pos[1]])
plt.tight_layout()