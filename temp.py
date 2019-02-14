from crawling_module import *
import sys

#print(sys.stdout.encoding)
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)
print(sys.stdout.encoding)
#export PYTHONIOENCODING=utf-8

req = requests.get('http://www.chictopia.com/browse/people/16?g=1')
html = req.text
soup = BeautifulSoup(html,'lxml')

#crawler('http://www.chictopia.com/photo/show/1154261-Public+Desire+ankle+boots-black-nasty-gal-top-dark-green-public-desire-boots')
#crawler('http://www.chictopia.com/photo/show/1154279-black+white+and+studded-black-forever-21-boots-eggshell-sheinside-sweater-neutral-balenciaga-bag')
#crawler('http://www.chictopia.com/photo/show/1154213-Kingdom+Collab+with+Coach-coach-sweater-pull-bear-shorts-coach-sneakers')

post_urls = soup.find_all('div', {'itemtype':"http://schema.org/Photograph"})
lst_post_url = []

for post_url in post_urls:
    lst_post_url.append('http://www.chictopia.com'+post_url.find('a').get('href'))

lst_post = []
for post_url in lst_post_url:    
    #post_id, title, photographer, lst_url, lst_size, lst_tag, lst_item = crawler(post_url)
    post_content = crawler(post_url)
    if post_content is None:
        continue
    lst_post.append(post_content)

#req = requests.get(page_url)
#html = req.text
#soup = BeautifulSoup(html,'lxml')

#crawler('http://www.chictopia.com/photo/show/1154261-Public+Desire+ankle+boots-black-nasty-gal-top-dark-green-public-desire-boots')
#crawler('http://www.chictopia.com/photo/show/1154279-black+white+and+studded-black-forever-21-boots-eggshell-sheinside-sweater-neutral-balenciaga-bag')
#crawler('http://www.chictopia.com/photo/show/1154213-Kingdom+Collab+with+Coach-coach-sweater-pull-bear-shorts-coach-sneakers')
#get_page('http://www.chictopia.com/browse/people/15?g=1')
