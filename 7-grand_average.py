#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 12:53:33 2020

@author: wexu
"""

import mne
from config_SYN_Human import study_path,exp
import os


ES_ID=exp[exp['group']=='ES'].index
ED_ID=exp[exp['group']=='ED'].index
IS_ID=exp[exp['group']=='IS'].index
ID_ID=exp[exp['group']=='ID'].index
       
GA_ES= mne.grand_average([mne.read_epochs(os.path.join(study_path,ID+"_ICA_cleaned-epo.fif")).average().apply_baseline((None,0)) for ID in ES_ID])
GA_ED= mne.grand_average([mne.read_epochs(os.path.join(study_path,ID+"_ICA_cleaned-epo.fif")).average().apply_baseline((None,0)) for ID in ED_ID])
GA_IS= mne.grand_average([mne.read_epochs(os.path.join(study_path,ID+"_ICA_cleaned-epo.fif")).average().apply_baseline((None,0)) for ID in IS_ID])
GA_ID= mne.grand_average([mne.read_epochs(os.path.join(study_path,ID+"_ICA_cleaned-epo.fif")).average().apply_baseline((None,0)) for ID in ID_ID])

GA_ES.comment='ES'
GA_ED.comment='ED'
GA_IS.comment='IS'
GA_ID.comment='ID'

GA_E= mne.grand_average([mne.read_epochs(os.path.join(study_path,ID+"_ICA_cleaned-epo.fif")).average().apply_baseline((None,0)) for ID in ES_ID.append(ED_ID)])
GA_I= mne.grand_average([mne.read_epochs(os.path.join(study_path,ID+"_ICA_cleaned-epo.fif")).average().apply_baseline((None,0)) for ID in IS_ID.append(ID_ID)])
GA_S= mne.grand_average([mne.read_epochs(os.path.join(study_path,ID+"_ICA_cleaned-epo.fif")).average().apply_baseline((None,0)) for ID in ES_ID.append(IS_ID)])
GA_D= mne.grand_average([mne.read_epochs(os.path.join(study_path,ID+"_ICA_cleaned-epo.fif")).average().apply_baseline((None,0)) for ID in ED_ID.append(ID_ID)])

mne.viz.plot_evoked_topo([GA_ES,GA_ED,GA_IS,GA_ID])

mne.viz.plot_evoked_topo([GA_E,GA_I])
mne.viz.plot_evoked_topo([GA_S,GA_D])

GA_EI_diff = mne.combine_evoked([GA_E, -GA_I], weights='equal')
GA_SD_diff = mne.combine_evoked([GA_S, -GA_D], weights='equal')

mne.viz.plot_evoked_topo([GA_EI_diff])
mne.viz.plot_evoked_topo([GA_SD_diff])


# for ID in ES_ID:
#     mne.viz.plot_evoked_topo(mne.read_epochs(os.path.join(study_path,ID+"_ICA_cleaned-epo.fif")).average().apply_baseline((None,0)),
#                              title=ID) 