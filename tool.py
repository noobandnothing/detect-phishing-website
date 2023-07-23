#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 01:45:57 2023

@author: noob
"""
from testdomain import testdomain
obj = testdomain("http://127.0.0.1/mytest/x.php")
X = obj.data
from joblib import load
clf = load('DTM.pkl')
Y = clf.predict([X])
print('# Decission Tree Classification : ')
if Y == -1 : 
    print("RESULT : NOT PHISHING")
else:
    print("RESULT : PHISHING")
model = load('LOM.pkl')
Ya = model.predict([X])
print('# Logistic Regression : ')
if Ya == -1 : 
    print("RESULT : NOT PHISHING")
else:
    print("RESULT : PHISHING")