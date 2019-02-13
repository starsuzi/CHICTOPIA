# -*- encoding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
from io import BytesIO
from PIL import Image

def crawler(post_url):

    req = requests.get(post_url)
    html = req.text 
    soup = BeautifulSoup(html, 'lxml')

    title, photographer = get_title_photographer(soup)
    lst_url = get_image_url(soup)
    lst_size = get_size(lst_url)
    lst_tag = get_tags(soup)
    lst_item = get_items(soup)

    return title, photographer, lst_url, lst_size, lst_tag, lst_item

def get_title_photographer(soup):

    photographer_and_title = soup.find('title').string.replace('"', '').split(' | ')[1].split(' by ')

    title = photographer_and_title[0]
    photographer = photographer_and_title[1]

    print(title)
    print(photographer)
    return title, photographer

def get_image_url(soup):
    
    lst_url = []

    img_urls = soup.find('div', {'style':'display:inline-block'})

    for img_url in img_urls:
        try:           
            lst_url.append(img_url.get('src').replace('_sm', ''))
        except :
            pass

    print(lst_url)
    return lst_url

def get_size(lst_url):

    lst_size = []

    for url in lst_url:
        image_raw = requests.get(url)
        image = Image.open(BytesIO(image_raw.content))
        #width, height = image.size
        lst_size.append(image.size)

    print(lst_size)
    return lst_size

def get_tags(soup):

    lst_tag = []
    tags = soup.find('div', {'class':'left clear px10'}).find_all('a')

    for tag in tags:
        lst_tag.append(tag.string)
    
    print(lst_tag)
    return lst_tag

def get_items(soup):

    lst_item = []
    items = soup.find_all('div', {'class':'garmentLinks left'})

    for item in items:
        str_item = ''
        item_names = item.find_all('a')
        for item_name in item_names:
            str_item = str_item + ' '+ item_name.string
        str_item = str_item[1:]
        lst_item.append(str_item)

    print(lst_item)
    return lst_item

crawler('http://www.chictopia.com/photo/show/1154261-Public+Desire+ankle+boots-black-nasty-gal-top-dark-green-public-desire-boots')
crawler('http://www.chictopia.com/photo/show/1154279-black+white+and+studded-black-forever-21-boots-eggshell-sheinside-sweater-neutral-balenciaga-bag')