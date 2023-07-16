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
######################### SOME PLOTTING ###########################
def ccp_alphas_VS_impurities():
    fig, ax = plt.subplots()
    ax.plot(ccp_alphas[:-1], impurities[:-1], marker="o", drawstyle="steps-post")
    ax.set_xlabel("effective alpha")
    ax.set_ylabel("total impurity of leaves")
    ax.set_title("Total Impurity vs effective alpha for training set")

ccp_alphas_VS_impurities()

##################### Get ALL POSSIBLE TREES ######################
clfs = []
for ccp_alpha in ccp_alphas:
    clf = DecisionTreeClassifier(random_state=0, ccp_alpha=ccp_alpha)
    clf.fit(X_train, y_train)
    clfs.append(clf)
######################### SOME PLOTTING ###########################

def nodes_depth_VS_aplha():
    node_counts = [clf.tree_.node_count for clf in clfs]
    depth = [clf.tree_.max_depth for clf in clfs]
    fig, ax = plt.subplots(2, 1)
    ax[0].plot(ccp_alphas, node_counts, marker="o", drawstyle="steps-post")
    ax[0].set_xlabel("alpha")
    ax[0].set_ylabel("number of nodes")
    ax[0].set_title("Number of nodes vs alpha")
    ax[1].plot(ccp_alphas, depth, marker="o", drawstyle="steps-post")
    ax[1].set_xlabel("alpha")
    ax[1].set_ylabel("depth of tree")
    ax[1].set_title("Depth vs alpha")
    fig.tight_layout()
    
nodes_depth_VS_aplha()
############### Calculate ALL posssible train and test ##############
train_scores = [clf.score(X_train, y_train) for clf in clfs]
test_scores = [clf.score(X_test, y_test) for clf in clfs]

##################### GET most MIN DIFFERENCE #######################
min = 0
for counter in range(1,len(train_scores)):
    if abs(train_scores[min]-test_scores[min]) >  abs(train_scores[counter]-test_scores[counter]):
        min = counter


def results_after_purn():
    fig, ax = plt.subplots()
    ax.set_xlabel("alpha")
    ax.set_ylabel("accuracy")
    ax.set_title("Accuracy vs alpha for training and testing sets")
    ax.plot(ccp_alphas, train_scores, marker="o", label="train", drawstyle="steps-post")
    ax.plot(ccp_alphas, test_scores, marker="o", label="test", drawstyle="steps-post")
    plt.axvline(x=ccp_alphas[min], color='red', linestyle='--')
    ax.legend()
    plt.show()
results_after_purn()
######################### MAKE MODEL #####################################
ccp_alpha_v = ccp_alphas[min]
clf = DecisionTreeClassifier(criterion="entropy",ccp_alpha=ccp_alpha_v)
clf = clf.fit(X_train, y_train)
print()
print("AFTER PRUNING :")
plot_diff(clf)

######################### MAKE TREE #####################################
from sklearn import tree
import graphviz 
fig = plt.figure(figsize=(25,20))
_ = tree.plot_tree(clf,fontsize=12,feature_names=clf.feature_names_in_)
dot_data = tree.export_graphviz(clf, out_file=None ,feature_names=clf.feature_names_in_)
graph = graphviz.Source(dot_data) 
graph.render("plot")
######################### Create PKL #####################################

import pickle
pickle.dump(clf, open('DTM.pkl','wb'))