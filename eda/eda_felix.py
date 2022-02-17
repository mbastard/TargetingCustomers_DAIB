# -*- coding: utf-8 -*-
"""
Created on Sun Feb  6 17:19:44 2022

@author: DE110456
"""
import pandas as pd
import numpy as np
import sys
path= "G:/My Drive/Uni Glasgow/DAIBI Data/"

sys.path.insert(0,'../utils')
  
# importing the utils_main library as utm
import utils_main as utm

import sys
sys.path.insert(1, './../utils/')
from utils_main import *

portfolio, profile, transcript = utm.readFiles(dropUnnecessaryCol = True)

portfolio = pd.read_json(path+'portfolio.json', lines=True)
profile = pd.read_json(path+'profile.json', lines=True)
transcript = pd.read_json(path+'transcript.json', lines=True)

# Rename Columns for the portfolio, profile, and transcript data frames
portfolio.rename(columns = {'id':'id_promotion'}, inplace = True)
profile.rename(columns = {'id':'id_membership'}, inplace = True)
transcript.rename(columns = {'person':'id_membership'}, inplace = True)

#### PROFILE DATA FRAME ####
# Change format of "became_member_on" attribute from int to datetime64[ns]
profile['became_member_on'] = pd.to_datetime(profile['became_member_on'], format='%Y%m%d')
# fill empty genders to "NA" string
profile['gender'] = profile['gender'].fillna('NA')



Portfolio_H=portfolio.head(20)
profile_H=profile.head(20)
transcript_H=transcript.head(20)
test["id"][1]


transcript ['freq'] = transcript .groupby('person')['person'].transform('count')
#histogram of number 
profile['age'].plot.hist(bins=25, alpha=0.5)


profile[profile.age == 118].shape[0]


utm.easy_histogram(profile,"age")
