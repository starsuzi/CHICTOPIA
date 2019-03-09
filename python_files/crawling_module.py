from bs4 import BeautifulSoup
import requests
from io import BytesIO
from PIL import Image
import sys
from multiprocessing import Pool, Manager
import random
import json
import codecs

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)

#function of getting next page url(man)
def get_next_page_man(page_num, category):
    
    base_page_url = 'http://www.chictopia.com/browse/people/'+category
    next_page_url = base_page_url +str(page_num)+'?g=2'

    return next_page_url

#function of getting next page url(woman)
def get_next_page_woman(page_num, category):
    
    base_page_url = 'http://www.chictopia.com/browse/people/'+category
    next_page_url = base_page_url +str(page_num)+'?g=1'

    return next_page_url

#function of getting the list of post urls of the page
def get_post_url(page_url):
    
    req = requests.get(page_url)
    html = req.text
    soup = BeautifulSoup(html,'lxml')

    post_urls = soup.find_all('div', {'itemtype':"http://schema.org/Photograph"})

    lst_post_url = []
    lst_delete = []

    for post_url in post_urls:
        lst_post_url.append('http://www.chictopia.com'+post_url.find('a').get('href'))
    
    for post_url in lst_post_url:
        lst_img_url = get_image_url(BeautifulSoup(requests.get(post_url).text, 'lxml'))

        if len(lst_img_url) < 3:
            lst_delete.append(post_url)

    lst_post_url = list(set(lst_post_url) - set(lst_delete))

    return lst_post_url

#getting each post in lst_post_url
def get_post(page_url):
     
    #get list of post urls from the page
    lst_post_url = get_post_url(page_url)
    lst_post = []

    #crawl the contents from the post url
    for post_url in lst_post_url:
        try:
            post_content = dict_to_json(crawler(post_url))
        except Exception as ex:
            print(ex)
            continue

        if post_content is None:  
            continue

        lst_post.append(post_content)

    return lst_post

#function for changing dictionary to json
def dict_to_json(dict_val):
    json_val = json.dumps(dict_val)
    return json_val

def crawler(post_url):

    req = requests.get(post_url)
    html = req.text 
    soup = BeautifulSoup(html, 'lxml')

     #get image url, title, photographer, tags and item from post_url
    lst_url = get_image_url(soup)
    title, photographer = get_title_photographer(soup)

    lst_tag = get_tags(soup)
    lst_item = get_items(soup)

    #get post_id
    post_id = post_url.split('/')[5]
    post_id = post_id.split('-')[0]

    return {"post_id":post_id, "post_url":'http://www.chictopia.com/photo/show/'+post_id, "img_url":lst_url, "tag": lst_tag, "item":lst_item}

#function for getting title and photographer
def get_title_photographer(soup):

    photographer_and_title = soup.find('title').string.replace('"', '').split(' | ')[1].split(' by ')
    title = photographer_and_title[0]
    photographer = photographer_and_title[1]

    print(title)
    return title, photographer

#function for getting image url
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

    return lst_url

#function for getting image size
def get_size(lst_url):

    lst_size = []

    for url in lst_url:
        image_raw = requests.get(url)
        image = Image.open(BytesIO(image_raw.content))
        lst_size.append(image.size)

    return lst_size

#function for getting tag
def get_tags(soup):

    lst_tag = []
    tags = soup.find('div', {'class':'left clear px10'}).find_all('a')

    for tag in tags:
        lst_tag.append(tag.string)

    return lst_tag

#function for getting items
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

#function for saving results of crawling according to category
def saver(category, total_page, percentage):
    lst_category_url_woman = ["http://www.chictopia.com/browse/people/clothes-"+category+"?g=1"]
    nested_nested_result = []
    flat_result = []

    for i in random.sample(range(total_page), int(total_page*percentage)):
        lst_category_url_woman.append(get_next_page_woman(i, 'clothes-'+category+'/'))

    p = Pool(16)
    res = p.map(get_post, lst_category_url_woman)
    if res is not None:
        nested_nested_result.append(res)
    
    for nested_sublist in nested_nested_result:
        for sublist in nested_sublist:
            for item in sublist:
                if len(set(flat_result)) == 1000:
                    break
                flat_result.append(item)


    print("===len===")
    print(len(flat_result))

    with open("./crawling_result/text/result_"+category+".txt", "w") as output:
        output.write(str(set(flat_result)))

#function for changing text to json
def text_to_json(category):
    
    text_file = './crawling_result/text/result_'+category+'.txt'
    json_file = './crawling_result/json/result_'+category+'.json'

    origin_file = open(text_file, 'r', encoding='utf-8')

    filedata = origin_file.read() 

    filedata = filedata.replace("}'", "}")
    filedata = filedata.replace("'{", "{")
    filedata = filedata.replace("{", '\n'+"{")
    filedata = filedata.replace('\\"', "")

    filedata = filedata.replace('"post_id"', '\n'+'"post_id"')
    filedata = filedata.replace('"post_url"', '\n'+'"post_url"')
    filedata = filedata.replace('"img_url"', '\n'+'"img_url"')
    filedata = filedata.replace('"tag"', '\n'+'"tag"')
    filedata = filedata.replace('"item"', '\n'+'"item"')

    filedata = filedata.replace("\\", "")
    filedata = filedata.replace("}, {", "}, "+"\n"+"{")

    filedata = filedata.replace(".jpg", '_400.jpg')

    filedata = filedata.replace('{'+'\n'+'{', '['+'\n'+'{')
    filedata = filedata.replace('}}', '}'+'\n'+']')

    saving_file = codecs.open(json_file, 'w', 'utf-8')
    saving_file.write(filedata)