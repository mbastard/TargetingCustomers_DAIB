# This python file contains functions for reading and preprocessing the raw data

import numpy as np
import pandas as pd


# Function reading the json raw files and doing some proprocessing
# Returns the preprocessed portfolio, profile, and transcript data frames
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
    transcript["id_promotion_rec"] = transcript["value"].apply(dict2Offerid) # promotion id for the offers received
    transcript["id_promotion_comp"] = transcript["value"].apply(dict2Offer_id) # promotion id for the offers completed
    transcript["amount"] = transcript["value"].apply(dict2Amount)
    transcript["reward"] = transcript["value"].apply(dict2Reward)
    
    # Drop Unncessary columns (i.e. extracted/split columns)
    if dropUnnecessaryCol == True:
        portfolio = portfolio.drop("channels",1)
        transcript = transcript.drop("value", 1)    
    
    return portfolio, profile, transcript

# Function extracting the "offer id" key for the "offer received" in the "value" dictionnary columns
# Returns the offer id or "" (i.e. empty string) if the key is not found
def dict2Offerid(dic):
    d = ""
    try:
        d = dic["offer id"]
    except:
        d = ""
    return d

# Function extracting the "offer_id" key for the "offer completed" in the "value" dictionnary columns
# Returns the offer id or "" (i.e. empty string) if the key is not found
def dict2Offer_id(dic):
    d = ""
    try:
        d = dic["offer_id"]
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
    
# Function deriving a set of informative variables that we can use to cluster customers
# The derived variables will start with "prep_" for preprocessing
# The derived variables are stored in the profile_prep data frame
def preprocessing(portfolio, profile, transcript, merge_how="outer"):
    
    #### TOTAL AVERAGE SPEND PER CUSTOMER ####
    #### prep_tot_aver_spend ####
    
    trans_mean = transcript.query('event == "transaction"') # Filter on transactions events
    trans_mean = trans_mean.groupby('id_membership').mean() # groupby id_membership and apply mean
    trans_mean = trans_mean.reset_index(level=[0]) # reset index
    trans_mean.rename(columns = {'amount':'prep_tot_aver_spend'}, inplace = True) # rename "amount" column to "prep_tot_aver_spend" column
    trans_mean = trans_mean[["id_membership", "prep_tot_aver_spend"]] # only keep the prep_tot_aver_spend and id_membership columns before merging
    
    profile_prep = pd.merge(trans_mean, profile, on="id_membership", how=merge_how) # Merge trans_mean and profile and strore the result in profile_prep
    
    #### TOTAL SPEND PER CUSTOMER ####
    #### prep_tot_spend ####
    
    trans_sum = transcript.query('event == "transaction"') # Filter on transactions events
    trans_sum = trans_sum.groupby('id_membership').sum() # groupby id_membership and apply sum
    trans_sum = trans_sum.reset_index(level=[0]) # reset index
    trans_sum.rename(columns = {'amount':'prep_tot_spend'}, inplace = True) # rename "amount" column to "prep_tot_spend" column
    trans_sum = trans_sum[["id_membership", "prep_tot_spend"]] # only keep the prep_tot_spend and id_membership columns before merging
    
    profile_prep = pd.merge(trans_sum, profile_prep, on="id_membership", how=merge_how) # Merge trans_sum and profile_prep and strore the result in profile_prep
    
    
    #### TOTAL NUMBER OF COMPLETED OFFER OVER THE SET PROMOTION PERIOD ####
    #### prep_nb_of_offer_comp ####
    
    trans_count = transcript.groupby(['id_membership', 'event']).count()
    trans_count_ind = trans_count.reset_index(level=[0,1]) # reset index
    trans_count_filt = trans_count_ind[trans_count_ind["event"] == "offer completed"] # Filter on "offer completed" only
    trans_count_filt.rename(columns = {'time':'prep_nb_of_offer_comp'}, inplace = True) # rename "time" column to "prep_nb_of_offer_comp" column
    trans_count_filt = trans_count_filt[["id_membership", "prep_nb_of_offer_comp"]] # only keep the prep_nb_of_offer_comp and id_membership columns before merging
    
    profile_prep = pd.merge(trans_count_filt, profile_prep, on="id_membership", how=merge_how) # Merge trans_count_filt and profile_prep and strore the result in profile_prep
    
    
    #### NUMBER OF TRANSACTIONS OVER THE SET PROMOTION PERIOD ####
    #### prep_nb_of_transactions ####
    
    trans_count = transcript.query('event == "transaction"') # Filter on transactions events
    trans_count = trans_count.groupby('id_membership').count() # groupby id_membership and apply count
    trans_count = trans_count.reset_index(level=[0]) # reset index
    trans_count.rename(columns = {'time':'prep_nb_of_transactions'}, inplace = True) # rename "time" column to "prep_nb_of_transactions" column
    trans_count = trans_count[["id_membership", "prep_nb_of_transactions"]] # only keep the prep_nb_of_transactions and id_membership columns before merging
    
    profile_prep = pd.merge(trans_count, profile_prep, on="id_membership", how=merge_how) # Merge trans_count and profile_prep and strore the result in profile_prep
    
    #### NUMBER OF OFFER RECEIVED OVER THE SET PROMOTION PERIOD ####
    #### prep_nb_of_offer_rec ####
    
    trans_count = transcript.query('event == "offer received"') # Filter on offer received events
    trans_count = trans_count.groupby('id_membership').count() # groupby id_membership and apply count
    trans_count = trans_count.reset_index(level=[0]) # reset index
    trans_count.rename(columns = {'time':'prep_nb_of_offer_rec'}, inplace = True) # rename "time" column to "prep_nb_of_offer_rec" column
    trans_count = trans_count[["id_membership", "prep_nb_of_offer_rec"]] # only keep the prep_nb_of_offer_rec and id_membership columns before merging
    
    profile_prep = pd.merge(trans_count, profile_prep, on="id_membership", how=merge_how) # Merge trans_count and profile_prep and strore the result in profile_prep
    
    
    #### NUMBER OF OFFER VIEWED OVER THE SET PROMOTION PERIOD ####
    #### prep_nb_of_offer_view ####
    
    trans_count = transcript.query('event == "offer viewed"') # Filter on offer viewed events
    trans_count = trans_count.groupby('id_membership').count() # groupby id_membership and apply count
    trans_count = trans_count.reset_index(level=[0]) # reset index
    trans_count.rename(columns = {'time':'prep_nb_of_offer_view'}, inplace = True) # rename "time" column to "prep_nb_of_offer_view" column
    trans_count = trans_count[["id_membership", "prep_nb_of_offer_view"]] # only keep the prep_nb_of_offer_view and id_membership columns before merging
    
    profile_prep = pd.merge(trans_count, profile_prep, on="id_membership", how=merge_how) # Merge trans_count and profile_prep and strore the result in profile_prep
    
    return profile_prep