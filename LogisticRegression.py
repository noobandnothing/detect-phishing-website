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
