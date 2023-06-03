# -*- coding: utf-8 -*-
"""Untitled11.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12w7RSmNOpI0IAvafLYHgGwf4dIP_NS6-
"""

# Import necessary libraries
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder,LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# importing Flask and other modules
from flask import Flask, request, render_template, send_from_directory
 
# Flask constructor
app = Flask(__name__)  

# Load the heart failure prediction dataset
df = pd.read_csv('heart.csv')
le = LabelEncoder()
# df['Sex'] = le.fit_transform(df['Sex'])
# Separate the features and labels
X = df.iloc[:, :-1]
y = df.iloc[:, -1]


# Convert categorical columns using one-hot encoding
# ct = ColumnTransformer([('encoder', OneHotEncoder(), [2, 6, 8, 10])], remainder='passthrough')
# X = ct.fit_transform(X)


# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

# Train a random forest classifier
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train_scaled, y_train)

# Evaluate the model on the test set
y_pred = rf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)


print(f'Test set accuracy: {accuracy:.4f}')

@app.route('/heart', methods =["GET", "POST"])
def heart():
    print("Serving")
    if request.method == "POST":
        # getting input with name = fname in HTML form
        para_value_a = request.form.get("")
        print(request.form)
        l = []
        for key,value in request.form.to_dict(flat=False).items():
            print (key, type(value))
            l += value
        l = scaler.transform([l])
        heart_result= rf.predict(l)
        if heart_result == [0]:
            return "Our prediction model suggests that you don't have a Heart disease. Nevertheless, we recommend that you speak to a healthcare professional if you have any concerns about your health."
            # return "Your result is:" + str(rfc.predict([l]))
        else:
            return "Based on the information you provided, our preliminary screening tool indicates that you may have a Heart Disease. Please seek medical advice from a qualified healthcare professional for further evaluation and testing."

@app.route('/<path:path>', methods =["GET", "POST"])
def paraphrase(path):
    print("Serving 2")
    print(path)
    return send_from_directory("Front end", path)


if __name__=='__main__':
   app.run(debug=True)


