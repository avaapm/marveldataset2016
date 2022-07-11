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

cat_page = 'https://www.shipspotting.com/photos/gallery?category='

for cat in cat_dict:
    cat_link = cat_page + str(cat_dict[cat])
    headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:96.0) Gecko/20100101 Firefox/96.0",
    "Referer": cat_link
}
#https://www.shipspotting.com/ssapi/gallery-search
    response = requests.get('https://www.shipspotting.com/js/vendors.2772b58b2400e824774d.js', headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    print(cat)