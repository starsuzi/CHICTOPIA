# -*- encoding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib.request
import requests

req = requests.get('http://www.chictopia.com/photo/show/1153101-Valentine%E2%80%99s+Day-dark-green-midi-zara-skirt-black-leather-zara-jacket')
html = req.text 

soup = BeautifulSoup(html, 'lxml')

photographer_and_title = soup.find('title').string.replace('"', '').split(' | ')[1].split(' by ')

title = photographer_and_title[0]
photographer = photographer_and_title[1]

print(title)
print(photographer)

lst_url = []

img_urls = soup.find('div', {'style':'display:inline-block'})

for img_url in img_urls:
    try:           
        #print(img_url.get('src'))
        lst_url.append(img_url.get('src').replace('_sm', ''))
    except :
        pass

#tag = soup.find('div', {'class':'left clear px10'})
#print(tag)

tags = soup.find('div', {'class':'left clear px10'}).find_all('a')

lst_tag = []

for tag in tags:
    lst_tag.append(tag.string)
print(lst_tag)

print(lst_url)

items = soup.find_all('div', {'class':'garmentLinks left'})
#print(items)
#items.find_all('a')
lst_item = []

for item in items:
    str_item = ''
    item_names = item.find_all('a')
    for item_name in item_names:
        str_item = str_item + ' '+ item_name.string
   # print(item_name)
    str_item = str_item[1:]
    #print(str_item)
    lst_item.append(str_item)

print(lst_item)