from crawling_module import *
import sys
import time
from multiprocessing import Pool, Manager
import itertools
import math

req = requests.get('http://www.chictopia.com/browse/people/600000?g=1')
html = req.text
soup = BeautifulSoup(html,'lxml')

soup.find('span', {'class':'current'}).text
#print(page_urls)