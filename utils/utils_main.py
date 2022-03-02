# This python file contains functions for reading and preprocessing the raw data


import numpy as np
import pandas as pd
import random
from lifetimes.utils import summary_data_from_transaction_data

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
    
    #### PROFILE DATA FRAME ####
    # Change format of "became_member_on" attribute from int to datetime64[ns]
    profile['became_member_on'] = pd.to_datetime(profile['became_member_on'], format='%Y%m%d')
    # fill empty genders to "NA" string
    profile['gender'] = profile['gender'].fillna('NA')
    
    #### TRANSCRIPT DATA FRAME ####
    # Extract values from the "value" dictionnary column into id_promotion, amount, and reward columns
    transcript["id_promotion_rec"] = transcript["value"].apply(dict2Offerid) # promotion id for the offers received
    transcript["id_promotion_comp"] = transcript["value"].apply(dict2Offer_id) # promotion id for the offers completed
    transcript["id_promotion"] = transcript["id_promotion_rec"] + transcript["id_promotion_comp"] # Combine promotion id for the offers received and completed
    transcript["amount"] = transcript["value"].apply(dict2Amount)
    transcript["reward_trans"] = transcript["value"].apply(dict2Reward)
    
    transcript.drop("id_promotion_rec", axis=1, inplace=True)
    transcript.drop("id_promotion_comp", axis=1, inplace=True)
    
    # Drop Unncessary columns (i.e. extracted/split columns)
    if dropUnnecessaryCol == True:
        transcript.drop("value", axis=1, inplace=True)
    
    return portfolio, profile, transcript


# Function to remove or impute missing values for the income column in the profile dataframe
def missingValuesProfileIncome(profile, how = 'remove'):

    # Remove all rows where the income is NaN
    if how == 'remove':
        profile = profile[profile['income'].notna()]

    # Replace the NaN values with the mean of the income
    elif how == 'impute':
        mean_income = profile['income'].mean()
        profile['income'] = profile['income'].fillna(mean_income)

    else:
        print("Please specify how = 'remove' or 'impute'!")

    return profile.copy()

# Function to remove or impute missing values for the gender column in the profile dataframe
def missingValuesProfileGender(profile, how = 'remove'):

    # Remove all rows where the income is "NA"
    if how == 'remove':
        profile = profile.query('gender != "NA"')

    # Replace the "NA" values with draws from "M", "F" and "O"
    elif how == 'impute':
        # Get the distribution of "M", "F" and "O"
        male_percentage = profile.query('gender != "NA"')['gender'].value_counts(normalize = True)["M"]
        female_percentage = profile.query('gender != "NA"')['gender'].value_counts(normalize = True)["F"]
        other_percentage = profile.query('gender != "NA"')['gender'].value_counts(normalize = True)["O"]

        # Replace "NA" values with a weighted random draw from ["M", "F", "O"]
        profile['gender'] = [random.choices(population = ['M', 'F', 'O'],
                                            weights = [male_percentage, female_percentage, other_percentage],
                                            k = 1)[0] if i == 'NA' else i for i in profile['gender'].to_list()]

    else:
        print("Please specify how = 'remove' or 'impute'!")
        
    return profile.copy()

# Function to remove or impute missing values for the age column in the profile dataframe
def missingValuesProfileAge(profile, how = 'remove'):

    # Remove all rows where the income is "118"
    if how == 'remove':
        profile = profile.query('age != 118')

    # Replace the "118" values with the mean of the age
    elif how == 'impute':
        mean_age = profile['age'].mean()
        profile['age'] = profile['age'].replace(118, np.nan)
        profile['age'] = profile['age'].fillna(mean_age)

    else:
        print("Please specify how = 'remove' or 'impute'!")

    return profile.copy()


# Function encoding categorical variables into binary variables
def oneHotEncoder(portfolio, profile, transcript, dropUnnecessaryCol=False):
    
    #### PORTFOLIO DATAFRAME ####
    
    # split channels column of lists into multiple binary columns (i.e. email, mobile, social, and web)
    portfolio["email"] = portfolio["channels"].apply(contains, testedChannel="email")
    portfolio["mobile"] = portfolio["channels"].apply(contains, testedChannel="mobile")
    portfolio["social"] = portfolio["channels"].apply(contains, testedChannel="social")
    portfolio["web"] = portfolio["channels"].apply(contains, testedChannel="web")
    # One-hot encoding of the offer_type column into discount, BOGO, and informational binary columns
    offer_type_dummies = portfolio['offer_type'].str.get_dummies()
    portfolio = pd.concat([portfolio,offer_type_dummies], axis=1)
    
    #### PROFILE DATAFRAME ####
    
    # gender type dummies
    profile['year_joined'] = profile['became_member_on'].apply(lambda x: str(x.year))

    gender_dummies = profile['gender'].str.get_dummies().add_prefix('gender_')
    year_joined_dummies = profile['year_joined'].str.get_dummies().add_prefix('year_joined_')

    profile = pd.concat([profile, gender_dummies, year_joined_dummies], axis=1)
    
    #### TRANSCRIPT DATAFRAME ####
    
    # event dummies
    event_dummies = transcript['event'].str.get_dummies()
    event_dummies.drop('transaction', axis=1, inplace=True)

    transcript = pd.concat([transcript, event_dummies], axis=1)
    transcript.rename(columns={'offer completed': 'offer_completed', 'offer received': 'offer_received', 'offer viewed': 'offer_viewed'}, inplace=True)

      
    # Drop Unncessary columns (i.e. extracted/split columns)
    if dropUnnecessaryCol == True:
        portfolio.drop("channels", axis=1, inplace=True)
        portfolio.drop("offer_type", axis=1, inplace=True)
        
        profile.drop(['gender'], axis=1, inplace=True)
        profile.drop(['became_member_on'], axis=1, inplace=True)
        profile.drop(['year_joined'], axis=1, inplace=True)
        
        #transcript.drop(['event'], axis=1, inplace=True)
        
    
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

# Function extracting and processing the transaction events from the transcript dataframe
def getTransactions(transcript, profile):
    transactions = transcript.query('event == "transaction"').copy()
    ##transactions['amount'] = transactions['value'].apply(lambda x: list(x.values())[0])
    #transactions.drop(['value', 'offer_completed', 'offer_received', 'offer_viewed'], axis=1, inplace=True)
    
    transactions = transactions.merge(profile, on="id_membership")
    #transactions.drop(['event'], axis=1, inplace=True)
    
    #### RECENCY AND FREQUENCY ####
    
    # time to Datetime
    # time is supposed to be in hours
    # Starting time is '2000-01-01' at 12
    transactions['datetime'] = transactions['time'].apply(lambda x: pd.Timestamp('2000-01-01T12') + pd.Timedelta(hours=x))

    rf = summary_data_from_transaction_data(transactions, 'id_membership', 'datetime', monetary_value_col='amount')
    rf = rf.reset_index(level=[0])
    #rf.drop('T', axis=1, inplace=True) # Drop T column :  This is equal to the duration between a customer’s first purchase and the end of the period under study

    #customers = profile.join(rf)
    customers = test = pd.merge(profile, rf, on="id_membership", how="outer")    
    
    return transactions, customers

# Function extracting and processing the NON-transaction events from the transcript dataframe
def getOffers(portfolio, profile, transcript):
    offers = transcript.query('event != "transaction"').copy()
    #offers['offer_id'] = offers['value'].apply(lambda x: list(x.values())[0])
    #offers.drop(['value'], axis=1, inplace=True)
    
    offers = pd.merge(offers, profile, on='id_membership', how="outer")
    offers = pd.merge(offers, portfolio, on='id_promotion', how="outer")
    offers.drop(['reward_trans'], axis=1, inplace=True)
    #offers.set_index('offer_id', inplace=True)
    #offers.head(2)
    
    return offers

# Function to create an easy histogram
def easy_histogram(dataframe,column):
    dataframe[column].plot.hist(bins=25, alpha=0.5)

