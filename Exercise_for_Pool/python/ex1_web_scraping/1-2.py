from time import sleep
import time
import re 
import random

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

t1 = time.time()
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
            print(driver.current_url)
            shop_name = driver.find_elements(By.CSS_SELECTOR,'p#info-name')
            if shop_name:
                shop_name = shop_name[0].text    
        
            tel = driver.find_elements(By.CSS_SELECTOR,'span.number')
            if tel:
                tel = tel[0].text
            else:
                tel = None
            #tel = re.sub('\n\t*',' ',tel)
            '''
            mail = driver.find_elements(By.CSS_SELECTOR,'a:-soup-contains("お店に直接メールする")')
            if mail:
                mail = mail[0].get_attribute('href')
            else:
                mail = None
            '''
            mail = None
            address = driver.find_elements(By.CSS_SELECTOR,'span.region')
            if address:
                address = address[0].text
                print(address)
                print(type(address))
                devided_address =  devide_address(address)
                prefecture = devided_address()[0]
                print(prefecture)
                district = devided_address()[1]
                print(district)
                number = devided_address()[2]
                print(number)
            else:
                prefecture = None
                district = None
                number = None
                    
            building = driver.find_elements(By.CSS_SELECTOR,'span.locality')
            if building:
                building = building[0].text
            else:
                building = None
                
            web_site = driver.find_elements(By.CSS_SELECTOR,'a.go-off')
            if web_site:
                web_site = web_site[0].get_attribute('href')
                if 'https' in web_site:
                    ssl = True
                else:
                    ssl = False
            else:
                web_site = None
                ssl = None
                
            
            d_list.append({
                '企業名':shop_name,
                '電話番号':tel,
                'メールアドレス':mail,
                '都道府県':prefecture,
                '市町村区':district,
                '番地':number,
                '建物名':building,
                'URL':web_site,
                'SSL証明書':ssl
            })
            print(len(d_list))
            if len(d_list) == 30:
                break
            driver.back()
    if len(d_list) == 30:
        break
    driver.find_element(By.CSS_SELECTOR,'ul.style_pages__Y9bbR > li:nth-of-type(10) > a').click()
    sleep(5)

df = pd.DataFrame(d_list)
df.to_csv('1-2.csv',index=None,encoding='utf-8-sig')

t2 = time.time()
print(t2-t1)
driver.quit()