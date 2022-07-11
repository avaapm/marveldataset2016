# this script collects the ID number from every desired category in the shipspotting dataset

from bs4 import BeautifulSoup
from urllib.request import urlopen, Request, build_opener, install_opener
from PIL import Image
import re
import json
# from matplotlib.font_manager import json_dump
import requests
import ssl 
ssl._create_default_https_context = ssl._create_unverified_context
import pandas as pd

num_imgs = 10000 # max 3444127

api_url= 'https://www.shipspotting.com/ssapi/gallery-search'
headers={'content-type': 'application/json'}
payload= {"category":"","perPage":12,"page":1}

df = pd.DataFrame(columns=['id','category','title'])

pages = num_imgs // 12 + 1

import numpy as np
database = np.zeros((num_imgs,3),dtype=object)

cnt = 0
for payload['page'] in range(1,pages):
    res=requests.post(api_url,headers=headers,json=payload, timeout=300)
    for item in res.json()['items']:
        database[cnt,0]=item['lid']
        database[cnt,1]=item['cid']
        database[cnt,2]=item['title']
        cnt+=1
        # line = pd.DataFrame([item['lid'],item['cid'],item['title']], columns=df.columns)
        # df = pd.concat([line,df], ignore_index=True)
    print('page:',payload['page'])

df = pd.DataFrame(database, columns=['id','category','title'])
df.to_csv('marvel_database.csv', index=False)
