import mailbox
from time import sleep
import time
import re 
import random
import shutil

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

def devide_address(address):
    #matches = re.match('(.{2,3}?[都道府県])(.+?郡.+?[町村]|.+?市.+?区|.+?[市区町村])(.+)',address)
    matches = re.match('(.{2,3}?[都道府県])(.+?郡.+?[町村]\D+|.+?市.+?区\D+|.+?[市区町村]\D+)([0-9]+-[0-9]+-[0-9]+|[0-9]+-[0-9]+|[0‐9]+-[0‐9]+‐[0-9]+|[0-9]+‐[0-9]+)',address)
    print(matches.groups)
    return matches.groups

user_agent = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
                  'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
                  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
                  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
                  ]

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('--user-agent=' + user_agent[random.randrange(0, len(user_agent), 1)])
driver = webdriver.Chrome(executable_path=r"C:\Users\taiha\Desktop\chromedriver\chromedriver.exe",options=options)
driver.implicitly_wait(10)

url = 'https://r.gnavi.co.jp/area/tokyo/japanese/rs/?p=1'
driver.get(url)
sleep(5)

d_list = []
while True:
    for i in range(24):
        print("="*30,i,"="*30)
        sleep(5)
        container = driver.find_elements(By.CSS_SELECTOR,'div.style_restaurant__SeIVn')[i]
        pr = container.get_attribute('data-restaurant-pr')
        if pr:
            continue
        else:
            driver.find_element(By.CSS_SELECTOR,'a.style_titleLink__oiHVJ').click()
            sleep(5)
            shop_name = driver.find_elements(By.CSS_SELECTOR,'p#info-name')
            if shop_name:
                shop_name = shop_name[0].text   

            mail = driver.find_elements(By.CSS_SELECTOR,'table.basic-table > tbody > tr:nth-of-type(12) > td > ul > li:nth-of-type(2) > a')
            if mail:
                mail = mail[0].get_attribute('href')
                print(mail)
            else:
                mail = None
                print(None)
                
            
            d_list.append({
                '企業名':shop_name,
                'メールアドレス':mail,
            })
            print(len(d_list))
            if len(d_list) == 20:
                break
            driver.back()
    if len(d_list) == 20:
        break
    driver.find_element(By.CSS_SELECTOR,'ul.style_pages__Y9bbR > li:nth-of-type(10) > a').click()
    sleep(5)

df = pd.DataFrame(d_list)
df.to_csv('test.csv',index=None,encoding='utf-8-sig')

#source = r"C:\Users\taiha\Desktop\Final-Answer\1-2.csv"
#destination = r"C:\Users\taiha\Desktop\Final-Answer\Exercise_for_Pool\python\ex1_web_scraping\1-2.csv"
#shutil.move(source,destination)

driver.quit()