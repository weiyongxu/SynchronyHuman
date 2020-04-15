#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 10:20:25 2020

@author: wexu
"""

import os 

study_path='/nashome1/wexu/MNE_data/SynchronyHuman2020/'

EEG_data_path = os.path.join(study_path, 'EEG')

import pandas as pd
exp=pd.read_excel('/nashome1/wexu/MNE_data/SynchronyHuman2020/dataInfo.xlsx',index_col=0)

exp=exp[exp['include']==True]


