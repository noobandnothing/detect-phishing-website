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



