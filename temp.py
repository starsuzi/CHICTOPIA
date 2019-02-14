from crawling_module import *
import sys
import time
from multiprocessing import Pool, Manager
import itertools
import math
'''
req = requests.get('http://www.chictopia.com/browse/people/2?g=1')
html = req.text
soup = BeautifulSoup(html,'lxml')

page_urls = soup.find('span', {'class':'current'}).text
print(page_urls)

lst_page_url = ['http://www.chictopia.com/browse/people?g=1']
page_num = 2
base_page_url = 'http://www.chictopia.com/browse/people/'

while True:

    next_page_url = base_page_url +str(page_num)+'?g=1'
    req = requests.get(next_page_url)
    html = req.text
    soup = BeautifulSoup(html, 'lxml')

    try:
        page_urls = soup.find('span', {'class':'current'}).text
        lst_page_url.append(next_page_url)
        #get_page(next_page_url)
        #print(next_page_url)
        print(page_num)
        page_num += 1
    except IndexError:
        print('finish')
        break
'''
def get_big_num():

    lst_big_num = []

    for i in range(2, sys.maxsize):
        #print(i)
        lst_big_num.append(i)
    return lst_big_num

def get_page_url(page_num):

    base_page_url = 'http://www.chictopia.com/browse/people/'

    next_page_url = base_page_url +str(page_num)+'?g=1'

    req = requests.get(next_page_url)
    html = req.text
    soup = BeautifulSoup(html, 'lxml')
        
    try:
        soup.find('span', {'class':'current'}).text
        print(page_num)

    except AttributeError:
        print('finish')
        return


if __name__ == '__main__':
    start_time = time.time()
    pool = Pool(processes=8)
    pool.map(get_page_url, range(0,10))
'''
if __name__ == '__main__':
    start_time = time.time()
    pool = Pool(processes=1)
    pool.map(get_page_url, range(0,10))
'''
#get_page_url(get_big_num())
# for i, page_num enumerate(get_big_num()):
