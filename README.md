# TargetingCustomers_DAIB


Targeting customers is an important marketing decision for most companies. The aim of this project is to identify
customer segments that a company can target in any marketing plans and the positioning of products.
A company recently introduced a variety of discount offers to members. Customers need to spend a certain amount
of money over a defined period of time. In return, the customer received a discount voucher. The company wants to
know which members responded best to this marketing campaign by spending more money.

## Environment

The "Readme_environment.md" file explains how you should set up your environment.

## Structure of the Repository

Folders:
* "data" contains the raw json files
* "eda" contains notebooks for the Exploratory Data Analysis phase
* "utils" contains diverse libraries (e.g. utils_main for reading and preprocessing the json files)
* "prep" contains the code to preprocess the data and to generate a common final dataset used for clustering
* "clustering" contains notebook sfor the Clustering phase

Files:
* "notes.md" contains all the goals (i.e. tasks) that have been set for the next meeting. This file contains also the findings that will be discussed during our weekly meetings.

## Data

The data for this project is available on Moodle under the group work project description folder. The data comprises
of three separate file described below. There is also an additional video explaining the data that can be found [here](https://www.youtube.com/watch?v=VVqsqOqfltU).


**portfolio.json** contains information about the ten promotions.
* **reward** is the monetary value of the promotion.
* **channels** is the ways in which the promotion was advertised. Created 4 new binary covariates after reading the file.
    * **email**
    * **mobile**
    * **social**
    * **web**
* **diffculty** is the amount the customer needs to spend in order to receive the reward.
* **duration** is the total number of days that the promotion was available.
* **offer_type** is the type of promotion. This is either a money off offer (**discount**), buy one get one free (**BOGO**) or
a news letter (**informational**).
* **id** is the promotion identitifcation -> renamed as **id_promotion** after reading the fie -> key link to transactions.json file


**transactions.json** contains information specific transaction across the promotion period.
* **person** is the customer membership identification -> renamed as **id_membership** after reading the file -> key link to profile.json file
* **event** is the event - either **offer received, offer viewed, offer complete** or **transaction**.
* **value.offer.id** is the promotion identification for received offers -> renamed as **id_promotion_rec** after reading the file -> key link to portfolio.json file
* **value.amount** is the amount spent in GBP for a given transaction -> renamed as **amount** after reading the file.
* **value.offer_id** is the promotion identification for completed offers -> renamed **id_promotion_comp** after reading the file -> key link to portfolio.json file
* **value.reward** is the monetary value of the promotion -> renamed as **reward** after reading the file.
* **time** time from the beginning of the promotion period (unit=day). time=0 would be the start of the promotional period and time=1 would be synonymous to day 1.


profile.json contains information about customers.
* **gender** is the identified gender of the customer.
* **age** is the age of the customer at the time of the promotion period.
* **id** is the customer membership identification -> renamed as **id_membership** after reading the file -> key link to transactions.json file
* **became_member** is the date when the customer became a member.
* **income** is the self reported income of the customer at the time of the promotion period.

## Learning objectives

## Question of interest
1. Identify clusters of customer that completed more transactions and/or spent more money over the promotional
period.
2. Provide an interpretation of clusters with visual representations of each cluster.
3. Provide a clear description of customer characteristics that the company should focus their attention to and
explain why.
You may find week 6 helpful in relation to this project.

## How to start

In order to complete this project, your group must derive a set of informative variables that you can use to cluster
customers into groups. Variables of interest may include, but certainly not limited to, the total average spend per
customer, the total number of completed offers, or the number of transactions over the set promotion period.

## Derived informative variables

These informative variables are derived while calling the preprocessing() fucntion in the utils/utils_main.py file

* prep_tot_aver_spend (same as monetary value) : TOTAL AVERAGE SPEND PER CUSTOMER
* prep_tot_aver_spend_discount : TOTAL AVERAGE SPEND ON DISCOUNT OFFERS PER CUSTOMER
* prep_tot_aver_spend_bogo : TOTAL AVERAGE SPEND ON BOGO OFFERS PER CUSTOMER
* prep_tot_spend : TOTAL SPEND PER CUSTOMER
* prep_nb_of_offer_rec : NUMBER OF OFFER RECEIVED OVER THE SET PROMOTION PERIOD
* prep_nb_of_offer_view : NUMBER OF OFFER VIEWED OVER THE SET PROMOTION PERIOD 
* prep_nb_of_offer_comp : TOTAL NUMBER OF COMPLETED OFFER OVER THE SET PROMOTION PERIOD
* prep_nb_of_transactions (same as frequency + 1) : NUMBER OF TRANSACTIONS OVER THE SET PROMOTION PERIOD
* prep_recency : age of the customer when they made their most recent purchases in number of days. This is equal to the duration between a customer’s first purchase and their latest purchase. (Thus if they have made only 1 purchase, the recency is 0. If they have made no purchase, the recency is -1)
* prep_T : age of the customer in days. This is equal to the duration between a customer’s first purchase and the end of the period under study. (If they have made no purchase, the recency is -1)

## Important links

* [Moodle - Forum - Anonymous discussion (e.g. time)](https://moodle.gla.ac.uk/mod/hsuforum/view.php?f=2383)

* [Moodle - Group work](https://moodle.gla.ac.uk/course/view.php?id=29456#section-2)

* [Youtube - Group description - Colette](https://www.youtube.com/watch?v=VVqsqOqfltU)

* [Medium - Starbucks offers](https://seifip.medium.com/starbucks-offers-advanced-customer-segmentation-with-python-737f22e245a4)
