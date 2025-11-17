#!/usr/bin/env python3
"""cleaning_script.py
Reads Mall_Customers.csv, performs cleaning, and writes cleaned_dataset.csv
Usage:
    python3 cleaning_script.py Mall_Customers.csv
If no argument provided it expects Mall_Customers.csv in the current directory.
"""
import sys, pandas as pd

path = sys.argv[1] if len(sys.argv) > 1 else 'Mall_Customers.csv'
df = pd.read_csv(path)

# Standardize column names
df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]

# Remove exact duplicates
df = df.drop_duplicates()

# Standardize gender values
def clean_gender(x):
    if pd.isnull(x): return pd.NA
    s = str(x).strip().lower()
    if s in ['m', 'male']: return 'Male'
    if s in ['f', 'female']: return 'Female'
    return pd.NA
df['gender'] = df['gender'].apply(clean_gender)

# Numeric parsing and median imputation
for col in ['age', 'annual_income_(k$)', 'spending_score_(1-100)']:
    df[col] = pd.to_numeric(df[col], errors='coerce')
    df[col] = df[col].fillna(df[col].median()).astype(int)

# Reorder columns for readability
df = df[['customerid', 'gender', 'age', 'annual_income_(k$)', 'spending_score_(1-100)']]

df.to_csv('cleaned_dataset.csv', index=False)
print('cleaned_dataset.csv written.')