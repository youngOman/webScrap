import requests
import time
from bs4 import BeautifulSoup
import os
import re
import urllib.request
import json

def get_web_page(url):
    resp=requests.get(url)
    if resp.status_code !=200:
        print('invalid url',resp.url)
        return None
    else:
        # print('ok')
        return resp.text

def get_shopitem(dom):
   
    soup = BeautifulSoup(dom,'html.parser')
    print(soup.prettify())

PCHOME_URL='https://shopping.pchome.com.tw/'
if __name__ == '__main__':
    current_page=get_web_page(PCHOME_URL+'search/v3.3/?q=鍵盤') 
    if current_page:
        keyboards=[]
        current_list=get_shopitem(current_page)
        keyboards+=current_list
        print(keyboards)
        