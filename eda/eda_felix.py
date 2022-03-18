# -*- coding: utf-8 -*-
"""
Created on Sun Feb  6 17:19:44 2022

@author: DE110456
"""
import numpy as np
import pandas as pd
import plotly.express as px
from pandas_profiling import ProfileReport

#change working directory
import os
os.getcwd()
os.chdir("C:/Users/de110456/Documents/GitHub/TargetingCustomers_DAIB/utils")

# importing the utils_main library
from utils_main import *
portfolio, profile, transcript = readFiles(dropUnnecessaryCol = False)

import utils_pipeline as utpi
import utils_plots as utpl

portfolio, profile, transcript = utpi.pipe_preProcessing(dropUnnecessaryCol = False, impute = True, how = 'impute')

