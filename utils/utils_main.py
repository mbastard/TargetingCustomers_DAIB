# This python file contains functions for reading and preprocessing the raw data

import numpy as np
import pandas as pd
import random
from lifetimes.utils import summary_data_from_transaction_data


# return the seed for all the random processes
def getSeed():
    return 1234

# Set seed for the random process
random.seed(getSeed()) 


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

    age_dummies = profile['age_cat'].str.get_dummies().add_prefix('age_cat_')
    income_dummies = profile['income_cat'].str.get_dummies().add_prefix('income_cat_')

    profile = pd.concat([profile, gender_dummies, year_joined_dummies, age_dummies, income_dummies], axis=1)

    # Drop unnessecary columns
    profile = profile.drop(['income_cat', 'age_cat'], axis=1)

    
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

#Function to categroize income into three categories
def income_categorizer(row, low, medium):

    if row['income'] < low:
        return 'low'

    elif row['income'] > low and row['income'] < medium:
        return 'medium'

    else:
        return 'high'

#Function to categroize age into three categories
def age_categorizer(row, low, medium):

    if row['age'] < low:
        return 'low'

    elif row['age'] > low and row['age'] < medium:
        return 'medium'

    else:
        return 'high'
    
# Function deriving a set of informative variables that we can use to cluster customers
# The derived variables will start with "prep_" for preprocessing
# The derived variables are stored in the profile_prep data frame
def preprocessing(portfolio, profile, transcript, merge_how="outer"):

    # Add column to categorize income into three categories low, medium and high
    low = profile['income'].quantile(0.33)
    medium = profile['income'].quantile(0.66)
    profile['income_cat'] = profile.apply(lambda row: income_categorizer(row, low, medium), axis=1)

    # Add column to categorize age into three categories low, medium and high
    low = 30
    medium = 50
    profile['age_cat'] = profile.apply(lambda row: age_categorizer(row, low, medium), axis=1)
    
    #### TOTAL AVERAGE SPEND PER CUSTOMER ####
    #### prep_tot_aver_spend ####
    
    trans_mean = transcript.query('event == "transaction"') # Filter on transactions events
    trans_mean = trans_mean.groupby('id_membership').mean() # groupby id_membership and apply mean
    trans_mean = trans_mean.reset_index(level=[0]) # reset index
    trans_mean.rename(columns = {'amount':'prep_tot_aver_spend'}, inplace = True) # rename "amount" column to "prep_tot_aver_spend" column
    trans_mean = trans_mean[["id_membership", "prep_tot_aver_spend"]] # only keep the prep_tot_aver_spend and id_membership columns before merging
    
    profile_prep = pd.merge(trans_mean, profile, on="id_membership", how=merge_how) # Merge trans_mean and profile and strore the result in profile_prep
    profile_prep['prep_tot_aver_spend'] = profile_prep['prep_tot_aver_spend'].fillna(0.0) ## Set null/Nan prep_tot_aver_spend to zero 
    
    #### TOTAL SPEND PER CUSTOMER ####
    #### prep_tot_spend ####
    
    trans_sum = transcript.query('event == "transaction"') # Filter on transactions events
    trans_sum = trans_sum.groupby('id_membership').sum() # groupby id_membership and apply sum
    trans_sum = trans_sum.reset_index(level=[0]) # reset index
    trans_sum.rename(columns = {'amount':'prep_tot_spend'}, inplace = True) # rename "amount" column to "prep_tot_spend" column
    trans_sum = trans_sum[["id_membership", "prep_tot_spend"]] # only keep the prep_tot_spend and id_membership columns before merging
    
    profile_prep = pd.merge(trans_sum, profile_prep, on="id_membership", how=merge_how) # Merge trans_sum and profile_prep and strore the result in profile_prep
    profile_prep['prep_tot_spend'] = profile_prep['prep_tot_spend'].fillna(0.0) ## Set null/Nan prep_tot_spend to zero 
    
    
    #### TOTAL NUMBER OF COMPLETED OFFER OVER THE SET PROMOTION PERIOD ####
    #### prep_nb_of_offer_comp ####
    
    trans_count = transcript.groupby(['id_membership', 'event']).count()
    trans_count_ind = trans_count.reset_index(level=[0,1]) # reset index
    trans_count_filt = trans_count_ind[trans_count_ind["event"] == "offer completed"] # Filter on "offer completed" only
    trans_count_filt.rename(columns = {'time':'prep_nb_of_offer_comp'}, inplace = True) # rename "time" column to "prep_nb_of_offer_comp" column
    trans_count_filt = trans_count_filt[["id_membership", "prep_nb_of_offer_comp"]] # only keep the prep_nb_of_offer_comp and id_membership columns before merging
    
    profile_prep = pd.merge(trans_count_filt, profile_prep, on="id_membership", how=merge_how) # Merge trans_count_filt and profile_prep and strore the result in profile_prep
    profile_prep['prep_nb_of_offer_comp'] = profile_prep['prep_nb_of_offer_comp'].fillna(0.0) ## Set null/Nan prep_nb_of_offer_comp to zero 
    
    
    #### NUMBER OF TRANSACTIONS OVER THE SET PROMOTION PERIOD ####
    #### prep_nb_of_transactions ####
    
    trans_count = transcript.query('event == "transaction"') # Filter on transactions events
    trans_count = trans_count.groupby('id_membership').count() # groupby id_membership and apply count
    trans_count = trans_count.reset_index(level=[0]) # reset index
    trans_count.rename(columns = {'time':'prep_nb_of_transactions'}, inplace = True) # rename "time" column to "prep_nb_of_transactions" column
    trans_count = trans_count[["id_membership", "prep_nb_of_transactions"]] # only keep the prep_nb_of_transactions and id_membership columns before merging
    
    profile_prep = pd.merge(trans_count, profile_prep, on="id_membership", how=merge_how) # Merge trans_count and profile_prep and strore the result in profile_prep
    profile_prep['prep_nb_of_transactions'] = profile_prep['prep_nb_of_transactions'].fillna(0.0) ## Set null/Nan prep_nb_of_transactions to zero 
    
    #### NUMBER OF OFFER RECEIVED OVER THE SET PROMOTION PERIOD ####
    #### prep_nb_of_offer_rec ####
    
    trans_count = transcript.query('event == "offer received"') # Filter on offer received events
    trans_count = trans_count.groupby('id_membership').count() # groupby id_membership and apply count
    trans_count = trans_count.reset_index(level=[0]) # reset index
    trans_count.rename(columns = {'time':'prep_nb_of_offer_rec'}, inplace = True) # rename "time" column to "prep_nb_of_offer_rec" column
    trans_count = trans_count[["id_membership", "prep_nb_of_offer_rec"]] # only keep the prep_nb_of_offer_rec and id_membership columns before merging
    
    profile_prep = pd.merge(trans_count, profile_prep, on="id_membership", how=merge_how) # Merge trans_count and profile_prep and strore the result in profile_prep
    profile_prep['prep_nb_of_offer_rec'] = profile_prep['prep_nb_of_offer_rec'].fillna(0.0) ## Set null/Nan prep_nb_of_offer_rec to zero 
    
    
    #### NUMBER OF OFFER VIEWED OVER THE SET PROMOTION PERIOD ####
    #### prep_nb_of_offer_view ####
    
    trans_count = transcript.query('event == "offer viewed"') # Filter on offer viewed events
    trans_count = trans_count.groupby('id_membership').count() # groupby id_membership and apply count
    trans_count = trans_count.reset_index(level=[0]) # reset index
    trans_count.rename(columns = {'time':'prep_nb_of_offer_view'}, inplace = True) # rename "time" column to "prep_nb_of_offer_view" column
    trans_count = trans_count[["id_membership", "prep_nb_of_offer_view"]] # only keep the prep_nb_of_offer_view and id_membership columns before merging
    
    profile_prep = pd.merge(trans_count, profile_prep, on="id_membership", how=merge_how) # Merge trans_count and profile_prep and strore the result in profile_prep
    profile_prep['prep_nb_of_offer_view'] = profile_prep['prep_nb_of_offer_view'].fillna(0.0) ## Set null/Nan prep_nb_of_offer_rec to zero 
    
    #### RECENCY and T OVER THE SET PROMOTION PERIOD ####
    #### prep_recency ####
    #### prep_T ####
    
    trans = transcript.query('event == "transaction"')
    # Suppose that time is in hours and the starting time is 2000-01-01
    trans['datetime'] = trans['time'].apply(lambda x: pd.Timestamp('2000-01-01T12') + pd.Timedelta(hours=x)) 
    rf = summary_data_from_transaction_data(trans, 'id_membership', 'datetime', monetary_value_col='amount')
    rf = rf.reset_index(level=[0])
    rf.rename(columns = {'recency':'prep_recency', 'T':'prep_T'}, inplace = True) # rename "time" column to "prep_nb_of_offer_rec" column
    
    profile_prep = pd.merge(rf[["id_membership", "prep_recency", "prep_T"]], profile_prep, on="id_membership", how=merge_how)
    profile_prep['prep_recency'] = profile_prep['prep_recency'].fillna(-1) ## Set null/Nan prep_recency to -1 - it means that no transaction has been performed 
    profile_prep['prep_T'] = profile_prep['prep_T'].fillna(-1) ## Set null/Nan prep_T to -1 - it means that no transaction has been performed 
    
    #### TOTAL AVERAGE SPEND ON DISCOUNT OFFERS PER CUSTOMER ####
    #### prep_tot_aver_spend_discount ####
    
    #### Reformating of the data ####
    
    transcript_merged = pd.merge(portfolio, transcript, on="id_promotion", how=merge_how) # merge on id_promotion
    offers = transcript_merged[transcript_merged.event != "transaction"]
    transactions = transcript_merged[transcript_merged.event == "transaction"]
    trans_offer = pd.merge(transactions[["time", "amount","id_membership"]], offers, on=["time", "id_membership"], how=merge_how)
    trans_offer = trans_offer[trans_offer.event == "offer completed"].copy()
    
    #### Compute prep_tot_aver_spend_discount ####
    
    trans_count_dis = trans_offer.query('offer_type == "discount"') # Filter on discount offer type
    trans_count_dis = trans_count_dis.groupby('id_membership').mean() # groupby id_membership and apply mean
    trans_count_dis = trans_count_dis.reset_index(level=[0]) # reset index
    
    trans_count_dis.rename(columns = {'amount_x':'prep_tot_aver_spend_discount'}, inplace = True) # rename "amount_x" column to "prep_tot_aver_spend_discount" column
    
    trans_count_dis = trans_count_dis[["id_membership", "prep_tot_aver_spend_discount"]] # only keep the prep_tot_aver_spend_discount and id_membership columns before merging 
    profile_prep = pd.merge(trans_count_dis, profile_prep, on="id_membership", how=merge_how) # Merge trans_count_dis and profile_prep and strore the result in profile_prep
    profile_prep['prep_tot_aver_spend_discount'] = profile_prep['prep_tot_aver_spend_discount'].fillna(0.0) ## Set null/Nan prep_tot_aver_spend_discount to zero 
    
    #### TOTAL AVERAGE SPEND ON BOGO OFFERS PER CUSTOMER ####
    #### prep_tot_aver_spend_bogo ####
    
    #### Compute prep_tot_aver_spend_bogo ####
    
    trans_count_bogo = trans_offer.query('offer_type == "bogo"') # Filter on discount offer type
    trans_count_bogo = trans_count_bogo.groupby('id_membership').mean() # groupby id_membership and apply mean
    trans_count_bogo = trans_count_bogo.reset_index(level=[0]) # reset index
    
    trans_count_bogo.rename(columns = {'amount_x':'prep_tot_aver_spend_bogo'}, inplace = True) # rename "amount_x" column to "prep_tot_aver_spend_bogo" column
    
    trans_count_bogo = trans_count_bogo[["id_membership", "prep_tot_aver_spend_bogo"]] # only keep the prep_tot_aver_spend_bogo and id_membership columns before merging 
    profile_prep = pd.merge(trans_count_bogo, profile_prep, on="id_membership", how=merge_how) # Merge trans_count_dis and profile_prep and strore the result in profile_prep
    profile_prep['prep_tot_aver_spend_bogo'] = profile_prep['prep_tot_aver_spend_bogo'].fillna(0.0) ## Set null/Nan prep_tot_aver_spend_bogo to zero 
    
    #### TOTAL AVERAGE REWARD ON COMPLETED OFFERS PER CUSTOMER ####
    #### prep_tot_aver_reward ####
    
    trans_mean = trans_offer.groupby('id_membership').mean() # groupby id_membership and apply mean
    trans_mean = trans_mean.reset_index(level=[0]) # reset index
    trans_mean.rename(columns = {'reward_trans':'prep_tot_aver_reward'}, inplace = True) # rename "reward_trans" column to "prep_tot_aver_reward" column
    trans_mean = trans_mean[["id_membership", "prep_tot_aver_reward"]] # only keep the prep_tot_aver_reward and id_membership columns before merging 


    profile_prep = pd.merge(trans_mean, profile_prep, on="id_membership", how=merge_how) # Merge trans_mean and profile_prep and store the result in profile_prep
    profile_prep['prep_tot_aver_reward'] = profile_prep['prep_tot_aver_reward'].fillna(0.0) ## Set null/Nan prep_tot_aver_reward to zero 
    
    
    #### TOTAL AVERAGE SPEND EXCLUDING OFFERS PER CUSTOMER ####
    #### prep_tot_aver_spend_exc_offers ####
    
    # Looking for the transactions that are not associated with any offer received, viewed or completed events #
    trans_count = transcript.groupby(["id_membership", "time"]).count()
    trans_count.reset_index(inplace=True)
    trans_count.rename(columns = {'event':'count_event'}, inplace = True)
    trans_count = trans_count[["id_membership", "time", "count_event"]]
    trans_count = pd.merge(trans_count, transcript, on=["id_membership", "time"], how=merge_how)
    trans_count = trans_count[trans_count["count_event"] == 1] # only keep transaction with 1 event (i.e. not associated with offer received, viewed or completed events)
    trans_count = trans_count[trans_count["event"] == "transaction"] # Only keep transaction event and NOT offer received, viewed or completed
    
    trans_mean = trans_count.groupby(["id_membership"]).mean()
    trans_mean.reset_index(level=[0], inplace=True)
    trans_mean.rename(columns = {'amount':'prep_tot_aver_spend_exc_offers'}, inplace = True)
    trans_mean = trans_mean[["id_membership", "prep_tot_aver_spend_exc_offers"]]
    
    profile_prep = pd.merge(trans_mean, profile_prep, on="id_membership", how=merge_how) # Merge trans_count_dis and profile_prep and strore the result in profile_prep
    profile_prep['prep_tot_aver_spend_exc_offers'] = profile_prep['prep_tot_aver_spend_exc_offers'].fillna(0.0) ## Set null/Nan prep_tot_aver_spend_exc_offers to zero 
    
    #### DELTA OF THE TOTAL AVERAGE SPEND BOGO AND THE TOTAL AVERAGE SPEND EXCLUDING OFFERS PER CUSTOMER ####
    #### delta_prep_tot_aver_spend_bogo_exc_offers ####
    #### Formula: prep_tot_aver_spend_bogo - prep_tot_aver_spend_exc_offers ####
    #Recommend to keep NAN values because assuming the value is 0 would dilute the power of the variable
    #Variable shows the difference between average spend with bogo offer compared to average spend with no offer 
    delta_prep=profile_prep[profile_prep["prep_tot_aver_spend_bogo"] !=0]
    delta_prep['delta_prep_tot_aver_spend_bogo_exc_offers']=delta_prep['prep_tot_aver_spend_bogo']-delta_prep['prep_tot_aver_spend_exc_offers']
    delta_prep.drop(delta_prep.columns.difference(['delta_prep_tot_aver_spend_bogo_exc_offers']), 1, inplace=True)
    profile_prep=profile_prep.join(delta_prep)
    #profile_prep['delta_prep_tot_aver_spend_bogo_exc_offers'] = profile_prep['delta_prep_tot_aver_spend_bogo_exc_offers'].fillna(0.0)
    
    #### DELTA OF THE TOTAL AVERAGE SPEND Discount AND THE TOTAL AVERAGE SPEND EXCLUDING OFFERS PER CUSTOMER ####
    #### delta_prep_tot_aver_spend_discount_exc_offers ####
    #### Formula: prep_tot_aver_spend_discount - prep_tot_aver_spend_exc_offers ####
    #Recommend to keep NAN values because assuming the value is 0 would dilute the power of the variable
    #Variable shows the difference between average spend with discount offer compared to average spend with no offer 
    delta_prep=profile_prep[profile_prep["prep_tot_aver_spend_discount"] !=0]
    delta_prep['delta_prep_tot_aver_spend_discount_exc_offers']=delta_prep['prep_tot_aver_spend_discount']-delta_prep['prep_tot_aver_spend_exc_offers']
    delta_prep.drop(delta_prep.columns.difference(['delta_prep_tot_aver_spend_discount_exc_offers']), 1, inplace=True)
    profile_prep=profile_prep.join(delta_prep)
    #profile_prep['delta_prep_tot_aver_spend_discount_exc_offers'] = profile_prep['delta_prep_tot_aver_spend_discount_exc_offers'].fillna(0.0)
    
    
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
    customers = pd.merge(profile, rf, on="id_membership", how="outer")    
    
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

