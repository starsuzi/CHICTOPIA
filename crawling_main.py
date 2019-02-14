from crawling_module import *
import sys

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)

def get_page(page_url):

    req = requests.get(page_url)
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

'''
total_page_num
pages = '/'.join[str(p) for p in ]

http://www.chictopia.com/browse/people?g=1
http://www.chictopia.com/browse/people/2?g=1

for page in pages:
'''
get_page('http://www.chictopia.com/browse/people?g=1')
page_num = 2
base_page_url = 'http://www.chictopia.com/browse/people/'

while True:
    
    try:
        next_page_url = base_page_url +str(page_num)+'?g=1'

        get_page(next_page_url)

        #print(next_page_url)
        print(page_num)
        page_num += 1
    except IndexError:
        break



