import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime
import os
import re
from urllib.request import urlretrieve
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
def get_article_list(dom):
    soup = BeautifulSoup(dom, features='lxml')
    item_blocks = soup.select('table.b-list tr.b-list-item')
    article_url_list = []
    for item_block in item_blocks:
        url_title = item_block.select_one('.b-list__main__title')  #文章網址
        article_url = f"https://forum.gamer.com.tw/{url_title.get('href')}"
        # url_title_name = item_block.select_one('.b-list__main__title').text  #文章標題名稱
        # push_count=item_block.find('span','b-list__summary__gp').text #推文數 select('.b-list__summary__gp')
        # Popularity=item_block.select_one('.b-list__count__number > span:last-of-type').text #擷取文章人氣值
        # Post_date_time=item_block.select_one('.b-list__time__edittime').text.strip() #發文日期及時間
        article_url_list.append(
            article_url #要取得內文時，只需取網址
            # 'url':article_url,
            # 'url_title_name':url_title_name,
            # 'push_count':push_count,
            # 'Popularity':Popularity, 
            # 'Post_date_time':Post_date_time,
        )
    return article_url_list
def get_article_detail(dom):
    resp = requests.get(dom, headers=HEADERS)
    if resp.status_code != requests.codes.ok:
        print('invalid url',resp.url)
        return None
    soup = BeautifulSoup(resp.text, features='lxml')
    article_title = soup.select_one('h1.c-post__header__title').text
    # article_total_page=get_article_total_page(soup) #討論串超過一頁再開
    # for page in range(article_total_page) #討論串超過一頁再開
        # article_detail_url = f"{dom}&page={page + 1}"
    reply_info_list=[]
    article_detail_url=(dom)
    reply_list=get_reply_info_list(article_detail_url)
    reply_info_list.extend(reply_list) #不會將整個串列帶進去List只會將值帶入
    time.sleep(1) #避免被認為是惡意爬蟲
    article_info={
        'a_title':article_title, #由於dict排序預設以字母排列，所以我在我想把要放在0,1的位置上的元素加上a
        'a_url':article_detail_url,
        'reply_list':reply_info_list,
    }
    # article_info.update({})
    return article_info
def get_reply_info_list(dom): #取得每一樓層的回覆
    resp = requests.get(dom, headers=HEADERS)
    if resp.status_code != requests.codes.ok:
        print('invalid url',resp.url)
        return None
    reply_info_list = []
    soup = BeautifulSoup(resp.text, features='lxml')
    reply_blocks=soup.select('section[id^="post_"]') #=post_開頭
    for reply_block in reply_blocks:
        reply_info = {}
        reply_info['floor'] = int(reply_block.select_one('.floor').get('data-floor')) #樓層
        reply_info['user_name'] = reply_block.select_one('.username').text #回覆者名稱
        reply_info['user_id'] = reply_block.select_one('.userid').text #回覆者id
        publish_time = reply_block.select_one('.edittime').get('data-mtime') #編輯日期&時間
        reply_info['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d %H:%M:%S') #轉換成datetime格式
        reply_info['content'] = reply_block.select_one('.c-article__content').text
        #取得推數
        gp_count = reply_block.select_one('.postgp span').text
        if gp_count == '-':
            gp_count = 0
        elif gp_count == '爆':
            gp_count = 1000
        reply_info['gp_count'] = int(gp_count)
        #取得倒讚數
        bp_count = reply_block.select_one('.postbp span').text
        if bp_count == '-':
            bp_count = 0
        elif bp_count == 'X': #倒讚倒500會變X
            bp_count = 500
        reply_info['bp_count'] = int(bp_count)
        reply_info_list.append(reply_info)

    return reply_info_list
# def get_article_total_page(dom): #討論串超過一頁再開
#     """取得文章總頁數"""
#     soup=BeautifulSoup(dom,features='lxml')
#     article_total_page = soup.select_one('.BH-pagebtnA > a:last-of-type').text #尾頁數
#     return int(article_total_page) #總共有幾頁
def get_img_url(dom):
    soup = BeautifulSoup(dom, 'html.parser')
    reply_blocks=soup.find('div',class_='c-post__body').find_all('a')
    img_urls=[]
    for reply_block in reply_blocks:
        if re.match(r'^https?://pbs.twimg.com/media/[A-Za-z0-9]+.jpg',reply_block['href']):
            img_urls.append(reply_block['href'])
    return img_urls

# print(soup.prettify()) #soup就是的html_doc解析的結果
# C.php?bsn=47157&snA=484&tnum=4 文章內文
# B.php?bsn=47157 文章列表
Game_URL='https://forum.gamer.com.tw/C.php?bsn=47157&snA=484&tnum=4'
if __name__ == '__main__':
    current_page=get_web_page(Game_URL)
    # if current_page: 
    dname=".\\星期一的豐滿"
    os.makedirs(dname)
    img_urls=get_img_url(current_page)
    for url in img_urls:
        fname = url.split('/')[-1]
        urlretrieve(url,os.path.join(dname,fname))
    # article_url_list=get_article_list(current_page) #所有文章的網址 || 文章列表的網址及資訊
    # -----從文章列表一一爬取"全部"文章的內文
    # for art_url in article_url_list:
    #     article_info=get_article_detail(art_url) #要爬取的文章url
    #     print(article_info)
    #     with open('bahaReplySection.json','a',encoding='UTF-8') as f: 
    #         json.dump(article_info,f,indent=2,sort_keys=True,ensure_ascii=False,default=str)
    # print(f"共爬了{len(article_url_list)} 篇文章")
    #-------取得文章列表資訊
    # arts=get_article_list(current_page)
    # with open('baha.json','w',encoding='UTF-8') as f:
    #     json.dump(arts,f,indent=2,sort_keys=True,ensure_ascii=False)

    # date = time.strftime("%m/%d").lstrip('0') 
    # parse(current_page)

    # article_info=get_article_detail(article_url_list[29]) #指定取得哪"一個"文章討論串內文
    # print(article_info['a_title'])

    # for data in article_info:
    #     print(data)
    
    

    # all_data=title_url|data #合併兩個dict
    # with open('bahaReplySection.json','w',encoding='UTF-8') as f: 
    #     json.dump(article_info,f,indent=2,sort_keys=True,ensure_ascii=False,default=str)




