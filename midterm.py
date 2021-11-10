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
def get_web_page(url):
    resp=requests.get(url,headers=HEADERS)
    if resp.status_code !=200:
        print('invalid url',resp.url)
        return None
    else:
        # print('ok') #成功取得網頁回應
        return resp.text
def get_article(dom):
    article_url_list = []
    soup = BeautifulSoup(dom, features='lxml')
    item_blocks = soup.select('table.b-list tr.b-list-item')
    for item_block in item_blocks:
        url_title = item_block.select_one('.b-list__main__title')  #文章網址
        push_count=item_block.find_all('span','b-list__summary__gp') #select('.b-list__summary__gp')
        for push in push_count:
            push=push #推數
        article_url = f"https://forum.gamer.com.tw/{url_title.get('href')}"
        article_url_list.append({
            'url':article_url,
            'push_count':push.text,
        })
    return article_url_list
# def article_info(dom):
def parse(dom):
    soup = BeautifulSoup(dom,'html.parser')
    links=soup.select_one('.c-section__main c-post')
    print(links)



# print(soup.prettify()) #soup就是的html_doc解析的結果

Game_URL='https://forum.gamer.com.tw/'
if __name__ == '__main__':
    current_page=get_web_page(Game_URL+'B.php?bsn=47157&subbsn=4') 
    get_article(current_page)
    if current_page:
        article_url_list=get_article(current_page)
        # print(article_url_list)
    parse(Game_URL+'C.php?bsn=47157&snA=485&tnum=3')
