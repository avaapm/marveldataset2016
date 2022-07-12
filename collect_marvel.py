# this script collects the ID number from every desired category in the shipspotting dataset

from bs4 import BeautifulSoup
import json
import requests
import ssl 
ssl._create_default_https_context = ssl._create_unverified_context
import pandas as pd
import numpy as np
import concurrent.futures

#first obtain a list of all categories
cats_link = 'https://www.shipspotting.com/photos/categories'

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:96.0) Gecko/20100101 Firefox/96.0",
}

soup = BeautifulSoup(requests.get(cats_link, headers=headers).text, 'html.parser')
script = soup.find_all('script')

script_txt = script[1].string[29:-7]

json_resp = json.loads(script_txt)

cat_dict = {}
for cat in json_resp['categories']:
    cat_dict[cat['title']] = cat['cid'] # dictionary with all the categories and their IDs

#remove unused categories
remove_list = [
    'Bulkers including more than one ship', 'Containerships (only) More than one vessel', 'Formation and group shots', 
    'General cargo ship photos, more than one ship', 'Harbour Overview Images', 'Historical / Unidentified Ship Funnel Marks',
    'Overview - fishing fleets', 'Reefers (only) more than one vessel', 'Ship Interior', "Ship's Deck", "Ship's engine rooms",
    'Shipping Companies Funnel Marks / Superstructure Logo Boards', 'Ships to be reclassified/waiting identity details',
    'Ships under Construction', 'Ships under Repair or Conversion', 'Storm Pictures', 'Wheelhouse', '_ Armaments',
    '_ For preservation', '_ Ships Crests', '_Flight Decks'
]

[cat_dict.pop(key) for key in remove_list]

df_all = pd.DataFrame(columns=['id','category','title'])

api_url= 'https://www.shipspotting.com/ssapi/gallery-search'
postheaders={'content-type': 'application/json'}

#Now collect the IDs for each category
# for cat in cat_dict:
def get_ids(cat):

    print('Collecting IDs for category: ' + cat)

    cat_link = 'https://www.shipspotting.com/photos/gallery?category=' + str(cat_dict[cat])
    soup = BeautifulSoup(requests.get(cat_link, headers=headers).text, 'html.parser')
    script = soup.find_all('script')
    script_txt = script[1].string[29:-7]
    json_resp = json.loads(script_txt)
    num_imgs = json_resp['photos']['count'] # obtain number of images per category

    pages = num_imgs // 12 + 1

    catdata = np.zeros((num_imgs,3),dtype=object)

    payload= {"category":str(cat_dict[cat]),"perPage":12,"page":1}

    cnt = 0
    for payload['page'] in range(1,pages):
        res=requests.post(api_url,headers=postheaders,json=payload, timeout=300)
        for item in res.json()['items']:
            catdata[cnt,0]=item['lid']
            catdata[cnt,1]=item['cid']
            catdata[cnt,2]=item['title']
            cnt+=1
        if payload['page'] % 10 == 0:
            print('page:',payload['page'])

    df_cat = pd.DataFrame(catdata, columns=['id','category','title'])
    df_cat.to_csv('category_data/' + cat + '.csv', index=False, header=False)

executor = concurrent.futures.ProcessPoolExecutor(10)
futures = [executor.submit(get_ids, cat) for cat in cat_dict]
concurrent.futures.wait(futures)