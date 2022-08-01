import pandas as pd

df = pd.read_csv('/home/davisac1/marvel_dataset.csv', names=['image_path','class_name','name', 'bbox', 'conf_score'])
#remove rows with bbox of []
df = df[df['bbox'] != '[]']

# df = df.drop('conf_score', axis=1)
df.to_csv('/home/davisac1/marvel_dataset_clean.csv', index=False, header=['image_path','class_name','name', 'bbox', 'conf_score'])