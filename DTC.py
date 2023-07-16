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


clf = DecisionTreeClassifier(criterion="entropy")
clf = clf.fit(X_train, y_train)
##################################################
def plot_diff(model):
    categories = ['Test', 'Train']
    print("TRAIN Accurecy : "+ str(model.score(X_train, y_train)))
    print("TEST Accurecy : "+ str(model.score(X_test, y_test)))
    values = [model.score(X_train, y_train) , model.score(X_test, y_test)]
    plt.bar(categories, values)
    plt.ylim(0, 2)
    plt.axhline(y=model.score(X_train, y_train), color='red', linestyle='--')
    plt.axhline(y=model.score(X_test, y_test), color='green', linestyle='--')
    # Add labels and title
    plt.xlabel('Type')
    plt.ylabel('SCORE')
    plt.title('Data scoring')
    plt.show()
##################################################
print()
print("BEFORE PRUNING :")
plot_diff(clf)
##################################################
path = clf.cost_complexity_pruning_path(X_train, y_train)
ccp_alphas, impurities = path.ccp_alphas, path.impurities
