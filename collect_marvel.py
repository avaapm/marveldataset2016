# this script collects the ID number from every desired category in the shipspotting dataset

from bs4 import BeautifulSoup
import json
import requests
import ssl 
ssl._create_default_https_context = ssl._create_unverified_context
import pandas as pd
import numpy as np
import concurrent.futures
import os

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
    'Mystery Ships',   'Overview - fishing fleets', 'Reefers (only) more than one vessel', 'Ship Interior', 
    "Ship's Deck", "Ship's engine rooms",    'Shipping Companies Funnel Marks / Superstructure Logo Boards', 'Ships to be reclassified/waiting identity details',    'Ships under Construction', 'Ships under Repair or Conversion', 'Storm Pictures', 'Wheelhouse', '_ Armaments',
    '_ For preservation', '_ Ships Crests', '_Flight Decks'
]

[cat_dict.pop(key) for key in remove_list]

df_all = pd.DataFrame(columns=['id','category','title'])

api_url= 'https://www.shipspotting.com/ssapi/gallery-search'
postheaders={'content-type': 'application/json'}

# cat_dict = {'Vehicle Carriers':12, 'Vegetable/Edible Oil Tankers':59, 'Inland Tugs':188, 'Tugs':10, 'Inland Passenger Vessels/ Ferries':184, 'Fishing vessel loa 70ft/21m and over':238,'Ferries':9, 'Fishing vessels loa less than 70ft/21m':239,'Chemical and Product Tankers':46,'Buoy/Lighthouse Maintenance Vessels & Lightships':202,'Construction Maintenance Vessels':277, 'Drilling Rigs/Parts of Drilling Rigs':94, 'Floating Production/Storage/Offloading Units':149,
# 'Floating Sheerlegs and Crane Barges/Crane Pontoons':41, 'Guard Vessels/Safety/Rescue':275, 'Harbour & tour boats / restaurant vessels':53, "Modern rig sailing ships / sailing yachts over 65' (20m) LOA":191, 'Reefers built 1980 onwards':224, 'RO/RO':21, 'Supply Ships/Tug Supplies/AHTS':35, 'Well Stimulation/Testing Vessels':280, 'Bulkers built 2001-2010':144, 'Bulkers built 2011-2020':257}

#Now collect the IDs for each category
# for cat in cat_dict:
def get_ids(cat):
    if (cat or cat.replace('/', '_')) in saved:
        print('Skipping category: ' + cat)
        return

    print('Collecting IDs for category: ' + cat)

    cat_link = 'https://www.shipspotting.com/photos/gallery?category=' + str(cat_dict[cat])
    soup = BeautifulSoup(requests.get(cat_link, headers=headers).text, 'html.parser')
    script = soup.find_all('script')
    script_txt = script[1].string[29:-7]
    json_resp = json.loads(script_txt)
    num_imgs = json_resp['photos']['count'] # obtain number of images per category

    pages = num_imgs // 12 + 1
    if pages > 1000:
        pages = 1000

    catdata = np.zeros((pages*12,3),dtype=object)

    payload= {"category":str(cat_dict[cat]),"perPage":12,"page":1}

    cnt = 0
    for payload['page'] in range(1,pages):
        res=requests.post(api_url,headers=postheaders,json=payload, timeout=300)
        for item in res.json()['items']:
            catdata[cnt,0]=item['lid']
            catdata[cnt,1]=item['cid']
            catdata[cnt,2]=item['title'].upper()
            cnt+=1
        if payload['page'] % 50 == 0:
            print(f'{cat} page: {payload["page"]}')

    df_cat = pd.DataFrame(catdata, columns=['id','category','title'])
    try:
        df_cat.to_csv('category_data/' + cat + '.csv', index=False, header=False)
    except:
        cat = cat.replace('/', '_')
        df_cat.to_csv('category_data/' + cat + '.csv', index=False, header=False)
    print('---- Saved category: ' + cat + ' ----')

saved = [savedcat[:-4] for savedcat in os.listdir('category_data')]

# while any(cat not in saved for cat in cat_dict): # retry if any category is not downloaded
    # executor = concurrent.futures.ThreadPoolExecutor(10)
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(get_ids, cat) for cat in cat_dict] 
    concurrent.futures.wait(futures) 
# saved = [savedcat[:-4] for savedcat in os.listdir('category_data')]