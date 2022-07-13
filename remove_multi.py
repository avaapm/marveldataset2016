import os
import pandas as pd

# remove listings with multiple ships in them to faciliate easy detection

cats = os.listdir('category_data')
for cat in cats:
    print('Processing category: ' + cat)
    df = pd.read_csv('category_data/' + cat, header=None)
    col = df.iloc[:,2]
    rows_no_amp = col.loc[col.str.find('&') == -1]
    rows_no_dash = col.loc[col.str.find(' - ') == -1]
    rows_no_and = col.loc[col.str.find(' AND ') == -1]
    rows_no_plus = col.loc[col.str.find('+') == -1]
    rows_to_save = [list(rows_no_amp.index),list(rows_no_dash.index),list(rows_no_and.index),list(rows_no_plus.index)]
    rows_to_save = list(set.intersection(*map(set, rows_to_save)))
    df = df.iloc[rows_to_save,:]
    df.to_csv('category_data/' + cat, index=False, header=False)
