from time import sleep
import re
from tokenize import group
import shutil

import requests
from bs4 import BeautifulSoup
import pandas as pd


def devide_address(address):
    #matches = re.match('(.{2,3}?[都道府県])(.+?郡.+?[町村]\D+|.+?市.+?区\D+|.+?[市区町村]\D+)([0-9]+-[0-9]+-[0-9]+|[0‐9]+-[0‐9]+‐[0-9]+)',address)
    matches = re.match('(.{2,3}?[都道府県])(.+?郡.+?[町村]\D+|.+?市.+?区\D+|.+?[市区町村]\D+)([0-9|-|‐]+)',address)
    return matches.groups

def correct_mail(mail):
    matche_mail = mail.replace('mailto:','')
    return matche_mail


base_url = 'https://r.gnavi.co.jp/area/tokyo/japanese/rs/?p={}'

d_list = []
for i in range(10):
    print(str(1+i)+'ページ目')
    url = base_url.format(1+i)
    sleep(3)
    res = requests.get(url,timeout=10)
    res.raise_for_status()
    soup = BeautifulSoup(res.content,'lxml')

    containers = soup.select('div.style_restaurant__SeIVn')
    for i,container in enumerate(containers):
        print('='*30,i,'='*30)
        pr = container.get('data-restaurant-pr')
        if pr:
            continue
        else:
            page_url = container.select_one('a.style_titleLink__oiHVJ').get('href')
            sleep(3)
            page_res = requests.get(page_url,timeout=30)
            page_res.raise_for_status()
            page_soup = BeautifulSoup(page_res.content,'lxml')

            shop_name = page_soup.select('p#info-name')
            if shop_name:
                shop_name = shop_name[0].text    
    
            tel = page_soup.select('span.number')
            if tel:
                tel = tel[0].text
            else:
                tel = None
            #tel = re.sub('\n\t*',' ',tel)

            mail = page_soup.select('a:-soup-contains("お店に直接メールする")')
            if mail:
                mail = mail[0].get('href')
                mail = correct_mail(mail)
            else:
                mail = None
                print(None)
            address = page_soup.select('span.region')
            if address:
                address = address[0].text
                devided_address =  devide_address(address)
                prefecture = devided_address()[0]
                district = devided_address()[1]
                number = devided_address()[2]
            else:
                prefecture = None
                district = None
                number = None
                
            building = page_soup.select('span.locality')
            if building:
                building = building[0].text
            else:
                building = None
            #a[class = "url go-off"]
            web_site = page_soup.select('a:-soup-contains("お店のホームページ")')
            if web_site:
                web_site = web_site[0].get('href')
                print(web_site)
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
            if len(d_list) == 50:
                break
    if len(d_list) == 50:
        break

df = pd.DataFrame(d_list)
df.to_csv('1-1.csv',index=None,encoding='utf-8-sig')

source = r"C:\Users\taiha\Desktop\Final-Answer\1-1.csv"
destination = r"C:\Users\taiha\Desktop\Final-Answer\Exercise_for_Pool\python\ex1_web_scraping\1-1.csv"
shutil.move(source,destination)