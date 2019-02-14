from crawling_module import *
import sys
from multiprocessing import Pool, Manager

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)

lst_page_url = ['http://www.chictopia.com/browse/people?g=1']

for i in range(2, 17714):
    lst_page_url.append(get_next_page(i))

#print(lst_page_url[17712])
#get_page('http://www.chictopia.com/browse/people/17713?g=1')

if __name__ == '__main__':
    pool = Pool(processes=5)
    pool.map(get_page, lst_page_url[2:5])
