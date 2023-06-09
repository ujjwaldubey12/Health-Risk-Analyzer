# -*- coding: utf-8 -*-
"""Liver.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1w9G5oewMZwnZnBPWtFWhI4kEhr6uKhkC
"""

# # Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
# from xgboost import XGBClassifier

# importing Flask and other modules
from flask import Flask, request, render_template, send_from_directory
 
# Flask constructor
app = Flask(__name__)  

# Load the dataset
data = pd.read_csv('Liver.csv', encoding='latin1')

# Data exploration
print(data.head())

# Check for missing values
print(data.isnull().sum())

# Data preprocessing
# Remove missing values
data.dropna(inplace=True)

# Convert categorical variables to numerical variables
# data['Gender of the patient'] = pd.get_dummies(data['Gender of the patient'], drop_first=True)
data['Result'] = pd.get_dummies(data['Result'], drop_first=True)

# Split the dataset into training and testing sets
X = data.drop(['Result'], axis=1)
y = data['Result']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the input variables
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Model training and evaluation
# Logistic regression
log_reg = LogisticRegression()
log_reg.fit(X_train_scaled, y_train)
y_pred = log_reg.predict(X_test_scaled)
print("Accuracy score for logistic regression:", accuracy_score(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Decision tree
tree = DecisionTreeClassifier()
tree.fit(X_train_scaled, y_train)
y_pred = tree.predict(X_test_scaled)
print("Accuracy score for decision tree:", accuracy_score(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Random forest
rfc = RandomForestClassifier()
rfc.fit(X_train_scaled, y_train)
y_pred = rfc.predict(X_test_scaled)
print("Accuracy score for random forest:", accuracy_score(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

# # XGBoost
# xgb = XGBClassifier()
# xgb.fit(X_train_scaled, y_train)
# y_pred = xgb.predict(X_test_scaled)
# print("Accuracy score for XGBoost:", accuracy_score(y_test, y_pred))
# print(confusion_matrix(y_test, y_pred))
# print(classification_report(y_test, y_pred))
# liver_result= rfc.predict(l)

@app.route('/liver', methods =["GET", "POST"])
def liver():
    print("Serving")
    if request.method == "POST":
        # getting input with name = fname in HTML form
        para_value_a = request.form.get("")
        print(request.form)
        l = []
        for key,value in request.form.to_dict(flat=False).items():
            print (key, type(value))
            l += value
        # l.pop(1)
        l = scaler.transform([l])
        liver_result= rfc.predict(l)
        if liver_result == [0]:
            return "Based on the information you provided, our preliminary screening tool indicates that you may have a liver disease. Please seek medical advice from a qualified healthcare professional for further evaluation and testing."
            # return "Your result is:" + str(rfc.predict([l]))
        else:
            return "Our prediction model suggests that you don't have a liver disease. Nevertheless, we recommend that you speak to a healthcare professional if you have any concerns about your health."

@app.route('/<path:path>', methods =["GET", "POST"])
def paraphrase(path):
    print("Serving 2")
    print(path)
    return send_from_directory("Front end", path)


if __name__=='__main__':
   app.run(debug=True)
