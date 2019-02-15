from crawling_module import *
import sys
from multiprocessing import Pool, Manager

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)

#lst_page_url = ['http://www.chictopia.com/browse/people?g=1']
lst_page_url = []

#for i in range(2, 17714):
#for i in range(2, 100):
#for i in range(100, 101):
#for i in range(101, 103):
#for i in range(103, 200):
#for i in range(2, 17714):
for i in range(11128, 17714):
    lst_page_url.append(get_next_page(i))

#print(lst_page_url[17712])
#get_page('http://www.chictopia.com/browse/people/17713?g=1')

#print(sys.getrecursionlimit())
if __name__ == '__main__':
    try:
        pool = Pool(processes=6)
        pool.map(get_page, lst_page_url[:])

    except Exception as ex:
        print('===================================')
        print(ex)
        print('===================================')
        pass
#17714