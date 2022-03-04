# This python file contains functions executing the pipelines for
# * the preprocessing of the portfolio, profile, transcript data frames (i.e. successively read files, impute missing values (optionnal), compute informative variables, do one-hot encoding)
# * the scaling and dimesionality reduction of the profile data frame

import utils_main as utm
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA

# Pre-Processing pipeline
# Function executing the preprocessing pipeline of the profile dataframe for the customers
# Successively read files, impute missing values (optionnal), compute informative variables, do one-hot encoding
def pipe_preProcessing(dropUnnecessaryCol = False, impute = True, how = 'impute'):
    # Read files
    portfolio, profile, transcript  = utm.readFiles(dropUnnecessaryCol = dropUnnecessaryCol)
    
    # Deal with missing values in the profile dataset (Optionnal)
    if impute == True:
        profile = utm.missingValuesProfileIncome(profile, how = how)
        profile = utm.missingValuesProfileGender(profile, how = how)
        profile = utm.missingValuesProfileAge(profile, how = how)
        
    # Pre-processing - compute informative variables
    profile = utm.preprocessing(portfolio, profile, transcript)
    
    # One-hot encoding
    
    portfolio, profile, transcript = utm.oneHotEncoder(portfolio, profile, transcript, dropUnnecessaryCol = dropUnnecessaryCol)
    
    return portfolio, profile, transcript     


# Pre-Modelling pipeline
# Function returning the scaled and the dimensionality reduced profile dataframe
# Successively scale the features and reduce the dimensionality of the profile data frame
def pipe_preMod(profile, var_explained=0.8):
    profile = profile.set_index("id_membership") # set id_membership as index
    
    # Apply feature scaling - leaving variances unequal is equivalent to putting more weight on variables with smaller variance
    scaler = StandardScaler().fit(profile)
    profile_scaled = scaler.transform(profile)
    
    # Apply dimensionality reduction -  k-means algorithm is both more effective and more efficient with a small number of dimensions
    # Use PCA to reduce dimensionality
    
    pca = PCA(random_state=utm.getSeed())
    X_pca = pca.fit_transform(profile_scaled)
    cum_expl_var_ratio = np.cumsum(pca.explained_variance_ratio_)
    num_components = len(cum_expl_var_ratio[cum_expl_var_ratio <= var_explained])
    
    # rerun PCA with components that explain 80% (default) of the variance
    pca = PCA(num_components).fit(profile_scaled)
    X_pca = pca.transform(profile_scaled)
    X_pca = pd.DataFrame(X_pca)
    
    return X_pca, pca
    