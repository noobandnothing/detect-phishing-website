#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Libraries
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
##################################################
data = pd.read_csv("phishing.csv")
X = data.drop(["class","Index"],axis =1)
y = data["class"]
##################################################
relations = data.corr().iloc[:-1,-1:]
relations = relations.sort_values(by=['class'],ascending=False)
X = X[relations[relations['class'] > 0.09].index]
##################################################
X_train, X_test , y_train, y_test = train_test_split(X, y, test_size = 0.2 ,random_state = 42)