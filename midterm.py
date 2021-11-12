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
        # Popularity=soup.select_one('.b-list__count__number > span').text #擷取文章人氣值
        # Post_date_time=item_block.select_one('.b-list__time__edittime').text.strip() #發文日期及時間
        article_url_list.append(
            article_url
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
        'title':article_title,
        'url':article_detail_url,
        'reply':reply_info_list,
    }
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

def parse(dom):
    soup = BeautifulSoup(dom, 'html.parser')   #另一個 parser
    links = soup.select('section[id^="post_"]').find_all('a')
    img_urls = []
    for link in links:
#       print("link:", link)
        if re.match(r'^https?://(i.)?(m.)?imgur.com', link['href']):
            img_urls.append(link['href'])
    return img_urls
def save(img_urls, title):
    if img_urls:
        try:
            title = title.replace("/", "-") 
            dname = title.strip()  # 用 strip() 去除字串前後的空白
            os.makedirs(dname)     # 建立資料夾
            for img_url in img_urls:
                print ("img_url_1", img_url)
                #'https://imgur.com/A2wmlqW.jpg'.split('//') 
                # -> ['https:', 'imgur.com/A2wmlqW.jpg']
                if img_url.split('//')[1].startswith('m.'): 
                    img_url = img_url.replace('//m.', '//i.')
                if not img_url.split('//')[1].startswith('i.'):
                    img_url = img_url.split('//')[0] + '//i.' + img_url.split('//')[1]
                 
                # 有時圖片沒有加上.jpg，將之補上
                if not img_url.endswith('.jpg'):
                    img_url += '.jpg'
                print ("img_url_2", img_url)
                fname = img_url.split('/')[-1]
                urlretrieve(img_url, os.path.join(dname, fname))
                #urllib.request.urlretrieve(url, filename): 將url表示的網絡對象複製到本地文件
                #os.path.join(dname, fname): 將路徑(dname)和檔案名稱(fname)結合為完整路徑
                
        except Exception as e:
            print(e)

# print(soup.prettify()) #soup就是的html_doc解析的結果
# C.php?bsn=47157&snA=484&tnum=4 文章內文
# B.php?bsn=47157 文章列表
Game_URL='https://forum.gamer.com.tw/B.php?bsn=47157'
if __name__ == '__main__':
    current_page=get_web_page(Game_URL)
    # if current_page: 
    article_url_list=get_article_list(current_page)
    # print(f"共爬取 {len(article_url_list)} 篇文章")
    # print(articles)

    # for article in articles:
    #     print(article)
    # with open('baha.json','w',encoding='UTF-8') as f:
    #     json.dump(articles,f,indent=2,sort_keys=True,ensure_ascii=False)

    # date = time.strftime("%m/%d").lstrip('0')  #
    # parse(current_page)
    # article_info(current_page)
    # print(article_info(current_page))

    article_info=get_article_detail(article_url_list[28]) #要爬取的文章index 
    title_url={'title':article_info['title'],'url':article_info['url']} #將title和url存成字典
    for data in article_info['reply']:
        print(data)
    all_data=title_url|data #合併兩個dict
    # print(all_data)
    with open('bahaReplySection.json','w',encoding='UTF-8') as f: 
        # json.dump(title_url,f,indent=2,sort_keys=True,ensure_ascii=False,default=str)
        json.dump(all_data,f,indent=2,sort_keys=True,ensure_ascii=False,default=str)

