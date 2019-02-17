from bs4 import BeautifulSoup
import requests
from io import BytesIO
from PIL import Image
import sys
from multiprocessing import Pool, Manager

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)

def get_next_page_man(page_num):
    
    base_page_url = 'http://www.chictopia.com/browse/people/'
    next_page_url = base_page_url +str(page_num)+'?g=2'

    return next_page_url

def get_page(page_url):
    
    print(page_url)

    req = requests.get(page_url)
    html = req.text
    soup = BeautifulSoup(html,'lxml')

    post_urls = soup.find_all('div', {'itemtype':"http://schema.org/Photograph"})

    lst_post_url = []
    for post_url in post_urls:
        lst_post_url.append('http://www.chictopia.com'+post_url.find('a').get('href'))

    #print('asdf')
    #print(lst_post_url)

    lst_post = []
    for post_url in lst_post_url:

            
        #post_id, title, photographer, lst_url, lst_size, lst_tag, lst_item = crawler(post_url)
        try:
            post_content = crawler(post_url)

        except Exception as ex:
            print(ex)
            continue

        if post_content is None:
            continue

        lst_post.append(post_content)

        #print('lst_post')
        #print(lst_post)
        #print('lst_post'+lst_post)
        
    return str(lst_post).encode('utf8')

        #lst_post.append('\n'.join(map(str, lst_post)))
    #print(lst_post)
    #print(type(lst_post))
    #lst_post = str(lst_post)
    
    #print(lst_post)

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

    #print(lst_item)
    return lst_item

#lst_page_url_man = ['http://www.chictopia.com/browse/people?g=2']


#for i in range(2, 936):
#for i in range(2, 100):
#for i in range(100, 300):
#for i in range(300, 500):
#for i in range(2, 500):
#for i in range(664, 900):
#for i in range(839, 900):
#for i in range(889, 936):

#print(lst_page_url[17712])
#get_page('http://www.chictopia.com/browse/people/17713?g=1')

if __name__ == '__main__':
    lst_page_url_man = ['http://www.chictopia.com/browse/people?g=2']
    result = []

    for i in range(2, 100 ):
        lst_page_url_man.append(get_next_page_man(i))


    p = Pool(10)
    result.append(p.map(get_page, lst_page_url_man))

    #print(lst_page_url_man)
    #print(result)
    with open("result_man.txt", "wb") as output:
        output.write(str(result).encode('utf8'))
'''
    except Exception as ex:
        print('===================================')
        print(ex)
        print('===================================')
        pass
        '''
'''
    result = []
    lst_page_url_man = []

    for i in range(2, 3):
        lst_page_url_man.append(get_next_page_man(i))

    try:
        pool = Pool(processes=4)
        result.append(pool.map(get_page, lst_page_url_man[:]))

    except Exception as ex:
        print('===================================')
        print(ex)
        print('===================================')
        pass

    print(result)

'''