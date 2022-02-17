# Formative Assessment
Febuary 21, 2022\
by Gabriel Berardi, Micheal Bastard and Felix von Wendorff

## Introduction
A cornerstone of every successful business is identifying potential customers, informing them of your service or product and hoping they become a customer. This process is called marketing. However, customers are complex and not all people are potential customers. The solution is targeted marketing; segmenting the population into distinct groups and approaching the ones most interested in the service. The emergence of internet advertainment has allowed for companies to target potential customers with greater precision than ever before. Data is now collected on advertisement conversion ratios allowing companies to know exactly how successful a marketing campaign was.\
The goal of this project is to segment a population of customers into categories based on what promotion they respond best to and identify the ideal promotion for each customer.  This project will attempt to cluster the customers into 11 groups, one for each promotion and one group for customer who do not respond to promotions. This is because a company should only market to those individuals where it believes it makes sense to promote to.

## Data
Three files are provided as data input: Portfolio, profile and transcript. Portfolio is a list of ten promotions that can be used to target the customers.  
The customers are listed in the profile data set and the transactions are listed in the transaction data set.

## Data Exploration
A total of 17,000 customers are identified in this project. Because the assignment is to subdivide the customers into distinct groups, the main goal is to have as much information about each customer as possible. By using the customer ID as a unique key, it is possible to link each customer to their transactions in the transaction data set and determine the total revenue generated from each customer.\
An immediate anomaly is that 2,175 individuals are listed as having an age of 118. These individuals do not have additional information available about them such as income or gender. It seems unlikely that this many 118 year old’s are customers and suggest that this is default value if age data is not given.  However, transactions are recorded so that it seems that these individuals are real people where the complete data about them is not known. Customers with an age of 118 do spend less and are a statistically distinct group. TO DO: T_TEST.\
![image](https://user-images.githubusercontent.com/47631827/154353983-05037655-25e8-483d-a400-cdba98cfe026.png)
\
Of the total 17,000, 422 have no recorded transactions, 4226 customers never responded to an offer, 6 did not receive any offers and 166 did not view any offer. 

## Data Cleaning

## Outlier Detection 

## Variables of Interest
After the total revenue per customer has been determined, it is possible to calculate the average revenue per year. This is important because it allows a long-term customer and a new customer to be compared in a fair manner.\
Another potential variable is the duration a customer has been a member. \
Finally, the number of transactions a customer initiated or number of  promotions a customer responded to could be an additional variable. By plotting two of these variables on a Cartesian plane, it is possible to segment them.

## Clustering Methodology
Two types of clustering were considered in this project: principal component analysis (PCA) and K-Means clustering. K-means analysis allows groups to appear in the scatterplot while PCA would enable the researchers to determine if a specific customer fits to a offer. 
