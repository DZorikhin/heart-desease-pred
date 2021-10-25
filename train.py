import pickle

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score


# parameters

C = 1.0
output_file = f'model_C={C}.bin'


# data preparation

df = pd.read_csv('framingham.csv')
df.drop(columns=['education'], inplace=True)
df['cigsPerDay'] = df['cigsPerDay'].fillna(0)
df['totChol'].fillna(value=df['totChol'].median(), inplace=True)
df['BMI'].fillna(value=df['BMI'].median(), inplace=True)
df['heartRate'].fillna(value=df['heartRate'].median(), inplace=True)
df['glucose'].fillna(value=df['glucose'].median(), inplace=True)
df['BPMeds'].fillna(0.0, inplace=True)

selected_f =  [
    'age', 'cigsPerDay', 'totChol', 'sysBP', 
    'BMI', 'heartRate', 'glucose', 'male', 
    'currentSmoker', 'BPMeds', 'prevalentStroke', 
    'prevalentHyp', 'diabetes'
]

df_full_train, df_test = train_test_split(df, test_size=0.2, random_state=13)
y_train_full = df_full_train.TenYearCHD.values
y_test = df_test.TenYearCHD.values
df_full_train = df_full_train[selected_f].reset_index(drop=True)
df_test = df_test[selected_f].reset_index(drop=True)


# train the final model

lr = LogisticRegression(C=0.1,
                        class_weight={0:1, 1:4}, 
                        max_iter=10000, 
                        random_state=13)
lr.fit(df_full_train.values, y_train_full)
y_pred = lr.predict_proba(df_test.values)[:, 1]
lr_auc = roc_auc_score(y_test, y_pred)
print(f'auc={lr_auc:.3f}')


# save the model

with open(output_file, 'wb') as f_out:
    pickle.dump(lr, f_out)

print(f'the model is saved to {output_file}')