import requests
import time
from bs4 import BeautifulSoup
import os
import re
import urllib.request
import json

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
}

url="https://www.juksy.com/channel/3C%E5%8B%95%E6%BC%AB"
resp=requests.get(url,headers=HEADERS)
if resp.status_code !=200:
    print('invalid url',resp.url)

else:
    print('ok') #成功取得網頁回應

soup = BeautifulSoup(resp.text, features='lxml')
item_blocks = soup.select('h3.title.line2')

# for item_block in item_blocks:
#     url_title = item_block.select_one() 
#     print(url_title)





