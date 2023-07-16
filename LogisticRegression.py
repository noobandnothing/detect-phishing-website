# -*- coding: utf-8 -*-
"""
Created on Thu May 25 11:22:39 2023

@author: MG Magic
"""

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("phishing.csv")
df.drop(columns = 'Index' , inplace = True)
X = df.iloc[0: , 0:30]
y = df.iloc[0: , 30]
#########################################################
relations = df.corr().iloc[:-1,-1:]
relations = relations.sort_values(by=['class'],ascending=False)
X = X[relations[relations['class'] > 0.09].index]
#########################################################
# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)
# Create and train the logistic regression model
model = LogisticRegression()
model.fit(X_train, y_train)

# Make predictions on the testing
y_pred = model.predict(X_test)

# Calculate the accuracy of the testing data
accuracy_testing = model.score(X_test, y_test)
print(f"Accuracy: {accuracy_testing}")

# Calculate the accuracy of the training data data
accuracy_training = model.score(X_train, y_train)
print(f"Accuracy: {accuracy_training}")
print("TRAIN Accurecy : "+ str(model.score(X_train, y_train)))
print("TEST Accurecy : "+ str(model.score(X_test, y_test)))

# Create pickle for model
import pickle
pickle.dump(model, open('LOM.pkl','wb'))

# Plotting score of train and score of test
plt.bar( ['training_Accuracy' , 'testing_accuracy'],[accuracy_training , accuracy_testing])
plt.ylim(0, 2)
plt.axhline(y=model.score(X_train, y_train), color='red', linestyle='--')
plt.axhline(y=model.score(X_test, y_test), color='green', linestyle='--')
# Add labels and title
plt.xlabel('Type')
plt.ylabel('SCORE')
plt.title('Data scoring')

# Plot relations
sns.heatmap(df.corr(), annot=True)
relations = df.corr()