#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 22:55:34 2020

@author: wexu
"""

import mne
from config_SYN_Human import study_path,exp
import os
import numpy as np

ES_ID=exp[exp['group']=='ES'].index
ED_ID=exp[exp['group']=='ED'].index
IS_ID=exp[exp['group']=='IS'].index
ID_ID=exp[exp['group']=='ID'].index


ES=np.array([mne.read_epochs(os.path.join(study_path,ID+"_ICA_cleaned-epo.fif")).average().apply_baseline((None,0)).crop(0.05,0.5).data for ID in ES_ID.append(ED_ID)])
IS=np.array([mne.read_epochs(os.path.join(study_path,ID+"_ICA_cleaned-epo.fif")).average().apply_baseline((None,0)).crop(0.05,0.5).data for ID in IS_ID.append(ID_ID)])

ES=ES.transpose([0, 2, 1])
IS=IS.transpose([0, 2, 1])

con,ch_names = mne.channels.find_ch_connectivity(mne.read_epochs(os.path.join(study_path,ES_ID[0]+"_ICA_cleaned-epo.fif")).info, "eeg")
# import matplotlib.pyplot as plt
# plt.imshow(con.toarray(), cmap='gray', origin='lower',interpolation='nearest')


t_obs, clusters, cluster_pv, h0=mne.stats.spatio_temporal_cluster_test([ES,IS],connectivity=con)

print('summary stats')
good_cluster_inds = np.where(cluster_pv < 0.05)[0]


#https://mne.tools/dev/auto_tutorials/stats-sensor-space/plot_stats_spatio_temporal_cluster_sensors.html#sphx-glr-auto-tutorials-stats-sensor-space-plot-stats-spatio-temporal-cluster-sensors-py