import os
import pandas as pd

"""In case you downloaded too much data, you can truncate the csv files"""

cat_data = 'category_data'
save_dir = 'category_data_trunc'

for file in os.listdir(cat_data):
    print('Processing file:', file)
    df = pd.read_csv(os.path.join(cat_data, file))
    df = df.iloc[0:12000]
    df.to_csv(os.path.join(save_dir, file), index=False)