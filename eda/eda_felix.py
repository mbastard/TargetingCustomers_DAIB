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



portfolio = pd.read_json(path+'portfolio.json', lines=True)
profile = pd.read_json(path+'profile.json', lines=True)
transcript = pd.read_json(path+'transcript.json', lines=True)

Portfolio_H=portfolio.head(20)
profile_H=profile.head(20)
transcript_H=transcript.head(20)
test["id"][1]


transcript ['freq'] = transcript .groupby('person')['person'].transform('count')
#histogram of number 
transcript['freq'].plot.hist(bins=25, alpha=0.5)


profile[profile.age == 118].shape[0]
