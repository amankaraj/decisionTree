A Decision Tree classifier is built for predicting credit worthiness of applicants.
Over fitting: The code prunes noisy data, it keeps track of the different set of values in the data and as soon as the count of positive and negative turns to become in the ratio of 1:9, the minority is considered as noise and return the majority.
In case there is Missing Data in the query, we consider all possible attribute value that can go in place of the ‘?’, calculate the classification for each of them and return the majority( positive and negative)

How to run: 
There are three type of files:
data.txt: This file contains the training data set.
Testing.txt: The file contains testing data.
Query.txt: The file contains data for query set.
In the Main.py file: To test the accuracy over the training data.
print QueryData.testTree() :To test the accuracy over the training data.
QueryData.query(): To run a new query.

