"""
This is the main script
"""
import pandas as pd

import dialog_extractor as de

df = pd.read_csv('test_data.csv')

# print(df)

features = df[df['role'] == 'manager']

features = de.get_info(features)
