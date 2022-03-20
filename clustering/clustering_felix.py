# -*- coding: utf-8 -*-
"""
Created on Sun Mar 20 16:39:44 2022

@author: DE110456
"""

import numpy as np
import pandas as pd
import random
import imp
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

from yellowbrick.cluster.elbow import kelbow_visualizer

import os
os.getcwd()
os.chdir("C:/Users/de110456/Documents/GitHub/TargetingCustomers_DAIB/utils")
# importing the utils_main library as utm
import utils_main as utm
import utils_pipeline as utpi
import utils_plots as utpl

from lifetimes.utils import summary_data_from_transaction_data

portfolio, profile, transcript = utpi.pipe_preProcessing(dropUnnecessaryCol = False, impute = True, how = 'impute')

profile = profile.drop(["year_joined", "gender", "became_member_on", "prep_tot_spend"], axis=1).copy()
#print(profile.isnull().sum())

X_pca, pca = utpi.pipe_preMod(profile, var_explained=0.8)
