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

    #print(title)
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

    with open("./crawling_result/text/result_"+category+".txt", "wb") as output:
        output.write('['+str(set(flat_result)).encode('utf8')+']')

#function for changing text to json
def text_to_json(category):
    
    text_file = './crawling_result/text/result_'+category+'.txt'

    json_file = './crawling_result/json/result_'+category+'_changed.json'

    s_file = open(text_file, 'r', encoding='utf-8')

    s_filedata = s_file.read() 

    s_filedata = s_filedata.replace("}'", "}")
    s_filedata = s_filedata.replace("'{", "{")
    s_filedata = s_filedata.replace("{", '\n'+"{")
    s_filedata = s_filedata.replace('\\"', "")

    s_filedata = s_filedata.replace('"post_id"', '\n'+'"post_id"')
    s_filedata = s_filedata.replace('"post_url"', '\n'+'"post_url"')
    s_filedata = s_filedata.replace('"img_url"', '\n'+'"img_url"')
    s_filedata = s_filedata.replace('"tag"', '\n'+'"tag"')
    s_filedata = s_filedata.replace('"item"', '\n'+'"item"')

    s_filedata = s_filedata.replace("\\", "")
    s_filedata = s_filedata.replace("}, {", "}, "+"\n"+"{")

    s_filedata = s_filedata.replace(".jpg", '_400.jpg')

    s_filedata = s_filedata.replace('{'+'\n'+'{', '['+'\n'+'{')
    s_filedata = s_filedata.replace('}}', '}'+'\n'+']')

    f_file = codecs.open(json_file, 'w', 'utf-8')
    f_file.write(s_filedata)

#main
if __name__ == '__main__':

    #dress
    #saver('dress',4322, 0.1) 
    #text_to_json('dress')

    #coat
    #saver('coat',1247, 1)     
    #text_to_json('coat')

    #vest
    #saver('vest',1247, 1)    
    #text_to_json('vest') 

    #jumper
    #saver('jumper',303, 1)
    #text_to_json('jumper')

    #skirt
    #saver('skirt',3495, 0.15)
    #text_to_json('skirt')
    
    #shirt
    #saver('shirt',2137, 0.25)
    #text_to_json('shirt')
    
    #blouse
    #saver('blouse',1515, 0.3)
    #text_to_json('blouse')
    
    #t-shirt
    #saver('t-shirt',1015, 0.5)
    #text_to_json('t-shirt')
    
    #sweater
    #saver('sweater',1581, 0.3)
    #text_to_json('sweater')   

    #top
    #saver('top',2700, 0.25)
    #text_to_json('top')  

    #jacket
    #saver('jacket',2079, 0.25)
    #text_to_json('jacket')  

    #blazer
    #saver('blazer',1198, 0.4) 
    #text_to_json('blazer')  

    #pants
    #saver('pants',1692, 0.3)
    #text_to_json('pants')  

    #jeans
    #saver('jeans',1720, 0.3)
    #text_to_json('jeans')  

    #shorts
    #saver('shorts',1675, 0.3)
    #text_to_json('shorts')   

    #panties
    #saver('panties',26, 1)
    #text_to_json('panties') 

    #leggings
    #saver('leggings',578, 1)
    #text_to_json('leggings') 

    #scarf
    #saver('scarf',820, 1)
    #text_to_json('scarf')

    #bag
    #saver('bag',3967, 0.15)
    #text_to_json('bag') 
    
    #purse
    #saver('purse',560, 1)
    #text_to_json('purse') 

    #shoes
    #saver('shoes',3887, 0.15)
    #text_to_json('shoes') 

    #sneakers
    #saver('sneakers',373, 1)
    #text_to_json('sneakers') 

    #boots
    #saver('boots',2840, 0.15)
    #text_to_json('boots') 

    #flats
    #saver('flats',387, 1)
    #text_to_json('flats') 

    #wedges
    #saver('wedges',490, 1)
    #text_to_json('wedges') 

    #sandals
    #saver('sandals',582, 1)
    #text_to_json('sandals') 

    #loafers
    #saver('loafers',135, 1)
    #text_to_json('loafers') 

    #clogs
    #saver('clogs',50, 1)
    #text_to_json('clogs') 

    #hat
    #saver('hat',1662, 0.3)
    #text_to_json('hat') 
     
    #glasses
    saver('glasses',247, 1)
    text_to_json('glasses') 


    