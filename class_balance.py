import os
import pandas as pd

#use this to see the class balance of the dataset before you download the data

cats = os.listdir('category_data')
counts = {}
for cat in cats:
    df = pd.read_csv('category_data/' + cat, header=None)
    num = len(df.index)
    counts[cat] = num

print(counts)