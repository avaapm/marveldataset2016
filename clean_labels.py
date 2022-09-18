import pandas as pd

df = pd.read_csv('/home/jovyan/pyspeir/pyspeir/datasets/marvel_dataset_clean.csv', names=['image_path','class_name','name', 'bbox', 'conf_score'])
#remove rows with bbox of []
# df = df[df['bbox'] != '[]']
# for i,path in enumerate(df['image_path']):
#     df['image_path'].iloc[i] = path
# df['image_path'].iloc[0] = str(df['image_path'].iloc[0].replace('\n','_'))#.replace({'/home/davisac1/':'/home/jovyan/data/'}).replace('\t','_').replace('?','_').replace('\\','').replace(':','_')
df['image_path']=df['image_path'].str.replace('/home/davisac1/','/home/jovyan/data/').replace('\t','_').replace('?','_').replace('\\','').replace(':''_').replace('\n','_')
df['image_path'] = df['image_path'].str.replace('\n','_')
df['name'] = df['name'].str.replace('\n','_')
# df['image_path'] = df.image_path.str.replace('\n','_').replace('/home/davisac1/','/home/jovyan/data/').replace('\t','_').replace('?','_').replace('\\','').replace(':','_')
print(df['image_path'].iloc[0]+'end')
print(df['name'].iloc[0]+'end')
# print(df['image_path'].iloc[0])
# df = df.drop('conf_score', axis=1)
df.to_csv('/home/jovyan/pyspeir/pyspeir/datasets/marvel_dataset_clean4.csv', index=False, header=None)