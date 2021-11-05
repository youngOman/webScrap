import requests
import re
import json
import csv
from bs4 import BeautifulSoup


Y_MOVIE_URL = 'https://tw.movies.yahoo.com/movie_thisweek.html'

# 以下網址後面加上 "/id=MOVIE_ID" 即為該影片各項資訊
# 供參考, 程式中未使用
Y_INTRO_URL = 'https://tw.movies.yahoo.com/movieinfo_main.html'  # 詳細資訊
Y_PHOTO_URL = 'https://tw.movies.yahoo.com/movieinfo_photos.html'  # 劇照
Y_TIME_URL = 'https://tw.movies.yahoo.com/movietime_result.html'  # 時刻表


def get_web_page(url):
    resp = requests.get(url)
    if resp.status_code != 200:
        print('Invalid url:', resp.url)
        return None
    else:
        return resp.text


def get_movies(dom):
    soup = BeautifulSoup(dom, 'html5lib')
    movies = []
    rows = soup.find_all('div', 'release_info_text')
    for row in rows:
        movie = dict()

        #中文名
        movie['ch_name'] = row.find('div', 'release_movie_name').a.text.strip()
        #英文名
        movie['eng_name'] = row.find('div', 'release_movie_name').find('div', 'en').a.text.strip()
        #期待度
        movie['expectation'] = row.find('div', 'leveltext').span.text.strip()
        #影片ID
        movie['movie_id'] = get_movie_id(row.find('div', 'release_movie_name').a['href'])
        #海報圖片
        movie['poster_url'] = row.parent.find_previous_sibling('div', 'release_foto').a.img['src']
        #上映日期
        movie['release_date'] = get_date(row.find('div', 'release_movie_time').text)
        #簡介
        movie['intro'] = row.find('div', 'release_text').text.replace(u'…', '').strip()
        # movie['intro'] = row.find('div', 'release_text').text.replace(u'詳全文', '').strip()
        #預告片網址
        trailer_a = row.find_next_sibling('div', 'release_btn color_btnbox').find_all('a')[1]
        movie['trailer_url'] = trailer_a['href'] if 'href' in trailer_a.attrs.keys() else ''
        
        movies.append(movie)  #movies是串列, 每一個元素是字典
    return movies


def get_date(date_str):
    # e.g. "上映日期：2017-03-23" -> match.group(0): "2017-03-23"
    pattern = '\d+-\d+-\d+'
    match = re.search(pattern, date_str)
    if match is None:
        return date_str
    else:
        return match.group(0)


def get_movie_id(url):
    # e.g., 'https://movies.yahoo.com.tw/movieinfo_main/%E6%AD%BB%E4%BE%8D2-deadpool-2-7820
    try:
        print('url:', url.split('-')[-1])
        movie_id = url.split('-')[-1]
        # print('url-:', url.split('.html')[0].split('-')[-1])
        # movie_id = url.split('.html')[0].split('-')[-1]  #此為原程式寫法
    except:
        movie_id = url
    return movie_id


if __name__ == '__main__':
    page = get_web_page(Y_MOVIE_URL)  #呼叫自訂方法, 傳入網址, 回傳網頁內容\
    #若有回傳網頁
    if page:
        movies = get_movies(page)     #呼叫自訂方法,解析網頁內容,取得電影的資料
        
        for movie in movies:
            print(movie)
        with open('movie.json', 'w', encoding='utf-8') as f:
            json.dump(movies, f, indent=2, sort_keys=True, ensure_ascii=False)
            
        f = open('movies.csv', 'w', encoding='utf-8',newline='') 
        csvWriter = csv.DictWriter(f, fieldnames = ['ch_name', 'eng_name', \
                                   'expectation','movie_id', 'poster_url', \
                                   'release_date', 'intro','trailer_url' ] )  # 指定欄位名稱    
        csvWriter.writeheader()    # 將欄位名稱寫入
        
        for movie in movies:
            csvWriter.writerow(movie)  
        f.close()


 