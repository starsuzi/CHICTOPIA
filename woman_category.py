from bs4 import BeautifulSoup
import requests
from io import BytesIO
from PIL import Image
import sys
from multiprocessing import Pool, Manager
import random

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)

def get_next_page_man(page_num):
    
    base_page_url = 'http://www.chictopia.com/browse/people/'
    next_page_url = base_page_url +str(page_num)+'?g=2'

    return next_page_url

def get_next_page_woman(page_num):
    
    base_page_url = 'http://www.chictopia.com/browse/people/'
    next_page_url = base_page_url +str(page_num)+'?g=1'

    return next_page_url

def get_post_url(page_url):
    
    req = requests.get(page_url)
    html = req.text
    soup = BeautifulSoup(html,'lxml')

    post_urls = soup.find_all('div', {'itemtype':"http://schema.org/Photograph"})
    #print(post_urls)
    lst_post_url = []
    for post_url in post_urls:
        lst_post_url.append('http://www.chictopia.com'+post_url.find('a').get('href'))

    return lst_post_url

def get_post(page_url):
        
    #print(page_url)

    req = requests.get(page_url)
    html = req.text
    soup = BeautifulSoup(html,'lxml')

    post_urls = soup.find_all('div', {'itemtype':"http://schema.org/Photograph"})
    #print(post_urls)
    lst_post_url = []
    for post_url in post_urls:
        lst_post_url.append('http://www.chictopia.com'+post_url.find('a').get('href'))

    lst_post = []
    for post_url in lst_post_url:
        #post_id, title, photographer, lst_url, lst_size, lst_tag, lst_item = crawler(post_url)
        #print(post_url)
        try:
            ##############
            post_content = crawler(post_url)

        except Exception as ex:
            print(ex)
            continue

        if post_content is None:  
            continue

        lst_post.append(post_content)

    return str(lst_post).encode('utf8')

def crawler(post_url):

    req = requests.get(post_url)
    html = req.text 
    soup = BeautifulSoup(html, 'lxml')

    lst_url = get_image_url(soup)

    if len(lst_url) < 3:
        #print(str(len(lst_url))+' images')
        #print('less than 3 images')
        return

    title, photographer = get_title_photographer(soup)
    lst_size = get_size(lst_url)
    lst_tag = get_tags(soup)
    lst_item = get_items(soup)

    post_id = post_url.split('/')[5]
    post_id = post_id.split('-')[0]

    return {'post_id':post_id, 'title':title, 'photographer':photographer, 'lst_url':lst_url, 'lst_size':lst_size, 'lst_tag':lst_tag, 'lst_item':lst_item}

def get_post_id(post_url):

    req = requests.get(post_url)
    html = req.text 
    soup = BeautifulSoup(html, 'lxml')

    lst_url = get_image_url(soup)

    if len(lst_url) < 3:
        #print(str(len(lst_url))+' images')
        #print('less than 3 images')
        return
    post_id = post_url.split('/')[5]
    post_id = post_id.split('-')[0]    


    print(post_id)
    #print(lst_url)    
    return post_id

def get_title_photographer(soup):

    photographer_and_title = soup.find('title').string.replace('"', '').split(' | ')[1].split(' by ')
    title = photographer_and_title[0]
    photographer = photographer_and_title[1]

    print(title)
    #print(photographer)
    return title, photographer

def get_image_url(soup):
    
    lst_url = []

    img_urls = soup.find('div', {'style':'display:inline-block'})

    if img_urls is None:
        return lst_url

    for img_url in img_urls:
        try:           
            lst_url.append(img_url.get('src').replace('_sm', ''))
        except :
            pass

    #print(lst_url)
    return lst_url

def get_size(lst_url):

    lst_size = []

    for url in lst_url:
        image_raw = requests.get(url)
        image = Image.open(BytesIO(image_raw.content))
        #width, height = image.size
        lst_size.append(image.size)

    #print(lst_size)
    return lst_size

def get_tags(soup):

    lst_tag = []
    tags = soup.find('div', {'class':'left clear px10'}).find_all('a')

    for tag in tags:
        lst_tag.append(tag.string)
    
    #print(lst_tag)
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

    return lst_item


if __name__ == '__main__':

    lst_dress_url_woman = ['http://www.chictopia.com/browse/people/clothes-dress?g=1']
    dress_result = []

    #dress
    lst_dress_page = random.sample(range(4322), 200)
    for i in lst_dress_page:
        lst_dress_url_woman.append(get_next_page_woman(i))

    p = Pool(16)
    dress_res = p.map(get_post_id_moreThan3, lst_dress_url_woman)

    #print(res)
    if dress_res is not None:
        dress_result.append(dress_res)

    print(dress_result)
    #print(result)
    #with open("list_woman_dress.txt", "wb") as output:
    #    output.write(str(result).encode('utf8'))



#http://www.chictopia.com/browse/people/clothes-dress?g=1
