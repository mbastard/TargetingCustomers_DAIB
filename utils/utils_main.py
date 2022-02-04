import numpy as np
import pandas as pd

def readFiles():
    # Read Files
    portfolio = pd.read_json('./../data/portfolio.json', lines=True)
    profile = pd.read_json('./../data/profile.json', lines=True)
    transcript = pd.read_json('./../data/transcript.json', lines=True)
    
    # Rename Columns
    portfolio.rename(columns = {'id':'id_promotion'}, inplace = True)
    profile.rename(columns = {'id':'id_membership'}, inplace = True)
    transcript.rename(columns = {'person':'id_membership'}, inplace = True)
    
    # Change format of "became_member_on" attribute from int to datetime64[ns]
    profile['became_member_on'] = pd.to_datetime(profile['became_member_on'].astype(str), format='%Y%m%d')
    
    # Split value dictionnary column into id_promotion, amount, and reward columns
    transcript["id_promotion"] = transcript["value"].apply(dict2Offerid)
    transcript["amount"] = transcript["value"].apply(dict2Amount)
    transcript["reward"] = transcript["value"].apply(dict2Reward)
    
    
    return portfolio, profile, transcript    


def dict2Offerid(dic):
    d = ""
    try:
        d = dic["offer id"]
    except:
        d = ""
    return d

def dict2Amount(dic):
    d = 0
    try:
        d = dic["amount"]
    except:
        d = 0
    return d

def dict2Reward(dic):
    d = 0
    try:
        d = dic["reward"]
    except:
        d = 0
    return d