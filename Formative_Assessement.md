# Formative Assessment
Febuary 21, 2022\
by Gabriel Berardi, Micheal Bastard and Felix von Wendorff

## Introduction
A cornerstone of every successful business is identifying potential customers, informing them of your service or product and hoping they become a customer. This process is called marketing. However, customers are complex and not all people are potential customers. The solution is targeted marketing; segmenting the population into distinct groups and approaching the ones most interested in the service. The emergence of internet advertainment has allowed for companies to target potential customers with greater precision than ever before. Data is now collected on advertisement conversion ratios allowing companies to know exactly how successful a marketing campaign was.\
The goal of this project is to segment a population of customers into categories based on what promotion they respond best to and identify the ideal promotion for each customer.  This project will attempt to cluster the customers into 11 groups, one for each promotion and one group for customer who do not respond to promotions. This is because a company should only market to those individuals where it believes it makes sense to promote to.

## Data
Three files are provided as data input: `portfolio`, `profile` and `transcript`. `portfolio` is a list of ten promotions that can be used to target the customers.  
The customers are listed in the `profile` data set and the `transactions` are listed in the `transcript` data set.

## Data Exploration
A total of 17,000 customers are identified in this project. Because the assignment is to subdivide the customers into distinct groups, the main goal is to have as much information about each customer as possible. By using the customer ID as a unique key, it is possible to link each customer to their transactions in the transaction data set and determine the total revenue generated from each customer.\
An immediate anomaly is that 2,175 individuals are listed as having an age of 118. These individuals do not have additional information available about them such as income or gender. It seems unlikely that this many 118 year old’s are customers and suggest that this is default value if age data is not given.  However, transactions are recorded so that it seems that these individuals are real people where the complete data about them is not known. Customers with an age of 118 do spend less and are a statistically distinct group. TO DO: T_TEST.\
![image](https://user-images.githubusercontent.com/47631827/154353983-05037655-25e8-483d-a400-cdba98cfe026.png)
\
Of the total 17,000, 422 have no recorded transactions, 4226 customers never responded to an offer, 6 did not receive any offers and 166 did not view any offer. 

## Data Cleaning - Outlier Detection and Missing Values
Successfully detecting outliers is a crucial step in any clustering project. For the purpose of this project, we defined outliers as datapoints lying outside the upper (Q3 + (1.5 * IQR)) and lower fence (Q1 – (1.5 * IQR)). Looking at the three datasets, we detected the following outliers:

### Portfolio
The portfolio dataset merely lists the ten different promotions and hence does not contain any outliers or missing values.

### Profile
In the profile dataset, we identified the following outliers:

**Age**\
The only outlier seems to be the age of 118. However, this corresponds to people where no gender and no income is recorded and could therefore be a systematic error, e.g. customers who chose to not disclose their age, gender and income. We decided to treat these entries as missing values and will impute values for these customers or remove these entries later on. When looking at the age per gender, there seem to be outliers for female customers where the age is 101:

<img src="./plots/profile_age_boxplot.png" alt="drawing" width="600"/>

However, these values are so close to the upper fence of the boxplot that we decided to keep these customers in the dataset.

**Income**\
When aggregated, there seems to be no outlier in terms of the income of the customers. However, when splitting the customers up by gender, there seem to be some outliers for male customers:

<img src="./plots/profile_income_boxplot.png" alt="drawing" width="600"/>

Similar to the outliers in the `age` column, these datapoints are so close to the upper fence and are still in a reasonable range that we decided to keep these entries.

### Transcript
In the transcript dataset we identified that the `amount` column is a highly right-skewed distribution with an extremely long tail:

<img src="./plots/transcript_amount_boxplot.png" alt="drawing" width="600"/>

However, the `transcript` dataset contains many transactions where the amount is equal to zero, in cases where an offer is completed. When we ignore these entries and zoom in on this, the distribution looks like this:

<img src="./plots/transcript_amount_histogram.png" alt="drawing" width="600"/>

From the structure of the data (e.g. "buy one get one" campaign type), we assume that the data stems from a retail food and beverage company and that high amount transactions could stem from large group orders or catering activities. Therefore, we will treat the `transcript` dataset as legitimate.

## Variables of Interest
After the total revenue per customer has been determined, it is possible to calculate the average revenue per year. This is important because it allows a long-term customer and a new customer to be compared in a fair manner.\
Another potential variable is the duration a customer has been a member. \
Finally, the number of transactions a customer initiated or number of  promotions a customer responded to could be an additional variable. By plotting two of these variables on a Cartesian plane, it is possible to segment them.

## Clustering Methodology
Two types of clustering were considered in this project: principal component analysis (PCA) and K-Means clustering. K-means analysis allows groups to appear in the scatterplot while PCA would enable the researchers to determine if a specific customer fits to a offer. 
