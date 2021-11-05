import requests
import time
from bs4 import BeautifulSoup
import os
import re
import urllib.request
import json

def get_web_page(url):
    resp = requests.get(
        url=url,
        cookies={'over18': '1'} #滿18歲以上
    )
    if resp.status_code != 200: #成功回傳200
        print('Invalid url:', resp.url)
        return None
    else:
        return resp.text


def get_articles(dom, date):
    soup = BeautifulSoup(dom, 'html5lib')

    # 取得上一頁的連結
    paging_div = soup.find('div', 'btn-group btn-group-paging')
    prev_url = paging_div.find_all('a')[1]['href']

    articles = []  # 儲存取得的文章資料
    divs = soup.find_all('div', 'r-ent')
    for d in divs:
        if d.find('div', 'date').text.strip() == date:  # 發文日期正確
            # 取得推文數
            push_count = 0
            push_str = d.find('div', 'nrec').text
            if push_str:
                try:
                    push_count = int(push_str)  # 轉換字串為數字
                except ValueError:
                    # 若轉換失敗，可能是'爆'或 'X1', 'X2', ...
                    # 若不是, 不做任何事，push_count 保持為 0
                    if push_str == '爆':
                        push_count = 99
                    elif push_str.startswith('X'):
                        push_count = -10

            # 取得文章連結及標題
            if d.find('a'):  # 有超連結，表示文章存在，未被刪除
                href = d.find('a')['href']
                title = d.find('a').text
                author = d.find('div', 'author').text if d.find('div', 'author') else ''
                articles.append({
                    'title': title,
                    'href': href,
                    'push_count': push_count,
                    'author': author
                })
    return articles, prev_url


def parse(dom):
    soup = BeautifulSoup(dom, 'html.parser')   #另一個 parser
    links = soup.find(id='main-content').find_all('a')
    img_urls = []
    for link in links:
#        print("link:", link)
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
                urllib.request.urlretrieve(img_url, os.path.join(dname, fname))
                #urllib.request.urlretrieve(url, filename): 將url表示的網絡對象複製到本地文件
                #os.path.join(dname, fname): 將路徑(dname)和檔案名稱(fname)結合為完整路徑
                
        except Exception as e:
            print(e)

PTT_URL = 'https://www.ptt.cc'

if __name__ == '__main__':
    current_page = get_web_page(PTT_URL + '/bbs/Tech_Job/index.html')
    if current_page:
        articles = []  # 全部的今日文章
        date = time.strftime("%m/%d").lstrip('0')  # 今天日期, 去掉開頭的 '0' 以符合 PTT 網站格式
        current_articles, prev_url = get_articles(current_page, date)  # 目前頁面的今日文章
        #測試用-只處理目前頁面的--------------------------------
        articles += current_articles
        print (articles)
        #測試用--------------------------------- 
        
#原本的程式先註解        
#        #若目前頁面有今日文章則加入 articles，並回到上一頁繼續尋找是否有今日文章
#        while current_articles:  
#            articles += current_articles
#            current_page = get_web_page(PTT_URL + prev_url)
#            current_articles, prev_url = get_articles(current_page, date)

        # 已取得文章列表，開始進入各文章讀圖
        for article in articles:
            print('\nProcessing', article)
            page = get_web_page(PTT_URL + article['href'])
            if page:
                #呼叫方法 parse處理圖片
                img_urls = parse(page)
                
                #將圖片存爝
                save(img_urls, article['title'])
                article['num_image'] = len(img_urls)

        print ("after:")
        print (articles)
