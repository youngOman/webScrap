from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest, time, re
import bs4
import csv
#我的chromedriver路徑
PATH = "./chromedriver"
driver = webdriver.Chrome(PATH)


driver.get("https://www.booking.com/index.zh-tw.html?aid=1725925;label=competitors-chinese-zh-xt-9Q88Z6LD74pzKEYVyiHCPwS533248621385:pl:ta:p1:p2:ac:ap:neg:fi:tikwd-97178419:lp9040380:li:dec:dm:ppccp=UmFuZG9tSVYkc2RlIyh9YbMgw1lSrhIuP8sID6VbpyE;ws=&gclid=CjwKCAiAm7OMBhAQEiwArvGi3J-eMa20ch50HOXOV2BnyN014CGBaiA_NDmRfaP3CNDm6y6_xJ6XIxoC8u0QAvD_BwE")
print(driver.title)
driver.find_element_by_id("xp__guests__toggle").click()
time.sleep(0.5)
driver.find_element_by_xpath("//form[@id='frm']/div/div[2]/div/div[3]/div/div/div/div/span").click()
time.sleep(0.5)
driver.find_element_by_xpath("//form[@id='frm']/div/div[2]/div[2]/div/div/div[3]/div/table/tbody/tr[3]/td[6]").click()
time.sleep(0.5)
driver.find_element_by_xpath("//form[@id='frm']/div/div[2]/div[2]/div/div/div[3]/div/table/tbody/tr[3]/td[7]/span/span").click()
time.sleep(0.5)
search = driver.find_element_by_name("ss")
search.send_keys("台中火車站")
time.sleep(0.5)
search.send_keys(Keys.RETURN)
'''#按下一頁，預計要3頁寫迴圈
count=0
while count<3:
    #讀取資料
    findData()
#以class搜尋，按下一頁
    driver.find_element_by_class_name("_ea2496c5b").click()
    count+=1
'''
def findData():
    f=open('hotel.csv', 'w', encoding='utf-8',newline='')
    csvWriter = csv.writer(f)
    csvWriter.writerow(['飯店名稱','價錢'])
    time.sleep(1.0)
    titles = driver.find_elements_by_css_selector("._c445487e2")
    prices = driver.find_elements_by_css_selector("._e885fdc12")    
    for title,price in zip(titles,prices):
        print(title.text,price.text)
        csvWriter.writerow([title.text,price.text])
    f.close()
findData()









