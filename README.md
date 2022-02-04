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

## Data

The data for this project is available on Moodle under the group work project description folder. The data comprises
of three separate file described below.


portfolio.json contains information about the ten promotions.
* reward is the monetary value of the promotion.
* channels is the ways in which the promotion was advertised.
* diffculty is the amount the customer needs to spend in order to receive the reward.
* duration is the total number of days that the promotion was available.
* offer_type is the type of promotion. This is either a money off offer (discount), buy one get one free (BOGO) or
a news letter (informational).
* id is the promotion identitifcation.


transactions.json contains information specific transaction across the promotion period.
* person is the customer membership identification.
* event is the event - either offer received, offer viewed, offer complete or transaction.
* value.offer.id is the promotion identification.
* value.amount is the amount spent in GBP for a given transaction.
* value.offer_id is the promotion identification.
* value.reward is the monetary value of the promotion.
* time time from the beginning of the promotion period.


profile.json contains information about customers.
* gender is the identified gender of the customer.
* age is the age of the customer at the time of the promotion period.
* id is the customer membership identification.
* became_member is the date when the customer became a member.
* income is the self reported income of the customer at the time of the promotion period.

## Learning objectives

## Question of interest
1. Identify clusters of customer that completed more transactions and/or spent more money over the promotional
period.
2. Provide an interpretation of clusters with visual representations of each cluster.
3. Provide a clear description of customer characteristics that the company should focus their attention to and
explain why.
You may find week 6 helpful in relation to this project.
How to start
In order to complete this project, your group must derive a set of informative variables that you can use to cluster
customers into groups. Variables of interest may include, but certainly not limited to, the total average spend per
customer, the total number of completed offers, or the number of transactions over the set promotion period.
