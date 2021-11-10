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

url="https://forum.gamer.com.tw/"
resp=requests.get(url,headers=HEADERS)
article_url_list = []
soup = BeautifulSoup(resp.text, features='lxml')
titles=soup.select("table.BH-table BH-table1 tr")
print(titles)
# print(item_blocks['href'])

# print(article_url_list,'ok')




