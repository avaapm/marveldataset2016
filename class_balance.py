import os
import pandas as pd
import numpy as np

#use this to see the class balance of the dataset before you download the data

cats = os.listdir('category_data')
print(cats)
counts = {}
for cat in cats:
    df = pd.read_csv('category_data/' + cat, header=None)
    num = len(df.index)
    counts[cat] = num

average = sum(counts.values()) / len(counts.values())

median = np.median(list(counts.values()))
total_counts = sum(counts.values())
num_classes = len(counts.values())
print(f'The average number of images per class is {average}')
print(f'The median number of classes is {median}')
print(f'The total number of images is {total_counts}')
print(f'The number of classes is {num_classes}')
df = pd.DataFrame.from_dict(counts, orient='index')