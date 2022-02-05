# This python file contains functions for reading and preprocessing the raw data

import numpy as np
import pandas as pd


# Function reading the json raw files and doing some proprocessing
# Returns the prrporcessed portfolio, profile, and transcript data frames
def readFiles(dropUnnecessaryCol = False):
    # Read Files
    portfolio = pd.read_json('./../data/portfolio.json', lines=True)
    profile = pd.read_json('./../data/profile.json', lines=True)
    transcript = pd.read_json('./../data/transcript.json', lines=True)
    
    # Rename Columns for the portfolio, profile, and transcript data frames
    portfolio.rename(columns = {'id':'id_promotion'}, inplace = True)
    profile.rename(columns = {'id':'id_membership'}, inplace = True)
    transcript.rename(columns = {'person':'id_membership'}, inplace = True)
    
    # portfolio data frame
    # split channels column of lists into multiple binary columns (i.e. email, mobile, social, and web)
    portfolio["email"] = portfolio["channels"].apply(contains, testedChannel="email")
    portfolio["mobile"] = portfolio["channels"].apply(contains, testedChannel="mobile")
    portfolio["social"] = portfolio["channels"].apply(contains, testedChannel="social")
    portfolio["web"] = portfolio["channels"].apply(contains, testedChannel="web")
    
    # profile data frame
    # Change format of "became_member_on" attribute from int to datetime64[ns]
    profile['became_member_on'] = pd.to_datetime(profile['became_member_on'].astype(str), format='%Y%m%d')
    
    # transcript data frame
    # Extract values from the "value" dictionnary column into id_promotion, amount, and reward columns
    transcript["id_promotion"] = transcript["value"].apply(dict2Offerid)
    transcript["amount"] = transcript["value"].apply(dict2Amount)
    transcript["reward"] = transcript["value"].apply(dict2Reward)
    
    # Drop Unncessary columns (i.e. extracted/split columns)
    if dropUnnecessaryCol == True:
        portfolio = portfolio.drop("channels",1)
        transcript = transcript.drop("value", 1)    
    
    return portfolio, profile, transcript

# Function extracting the "offer id" key in the "value" dictionnary columns
# Returns the offer id or "" (i.e. empty string) if the key is not found
def dict2Offerid(dic):
    d = ""
    try:
        d = dic["offer id"]
    except:
        d = ""
    return d

# Function extracting the "amount" key in the "value" dictionnary columns
# Returns the amount or 0 if the key is not found
def dict2Amount(dic):
    d = 0
    try:
        d = dic["amount"]
    except:
        d = 0
    return d

# Function extracting the "reward" key in the "value" dictionnary columns
# Returns the reward or 0 if the key is not found
def dict2Reward(dic):
    d = 0
    try:
        d = dic["reward"]
    except:
        d = 0
    return d

# Function testing if the testeChannel (e.g. email) is constained in the passed list
def contains(channels, testedChannel="email"):
    r = 0
    if testedChannel in channels:
        r = 1
    return r
    
