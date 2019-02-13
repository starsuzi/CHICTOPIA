# -*- encoding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
from io import BytesIO
from PIL import Image

req = requests.get('http://www.chictopia.com/photo/show/1154261-Public+Desire+ankle+boots-black-nasty-gal-top-dark-green-public-desire-boots')
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

print(lst_url)

lst_size = []

for url in lst_url:
    image_raw = requests.get(url)
    image = Image.open(BytesIO(image_raw.content))
    #width, height = image.size
    lst_size.append(image.size)

print(lst_size)

tags = soup.find('div', {'class':'left clear px10'}).find_all('a')

lst_tag = []

for tag in tags:
    lst_tag.append(tag.string)
print(lst_tag)

lst_item = []
items = soup.find_all('div', {'class':'garmentLinks left'})

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

