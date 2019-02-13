from crawling_module import *

req = requests.get('http://www.chictopia.com/browse/people')
html = req.text
soup = BeautifulSoup(html,'lxml')

#crawler('http://www.chictopia.com/photo/show/1154261-Public+Desire+ankle+boots-black-nasty-gal-top-dark-green-public-desire-boots')
#crawler('http://www.chictopia.com/photo/show/1154279-black+white+and+studded-black-forever-21-boots-eggshell-sheinside-sweater-neutral-balenciaga-bag')
#crawler('http://www.chictopia.com/photo/show/1154213-Kingdom+Collab+with+Coach-coach-sweater-pull-bear-shorts-coach-sneakers')

post_urls = soup.find_all('div', {'itemtype':"http://schema.org/Photograph"})
lst_post_url = []
#print(post_urls)
for post_url in post_urls:
    lst_post_url.append('http://www.chictopia.com'+post_url.find('a').get('href'))

#print(lst_post_url)

for post_url in lst_post_url:    
    #post_id, title, photographer, lst_url, lst_size, lst_tag, lst_item = crawler(post_url)
    crawler(post_url)
#print(post_id)
#for post_url in lst_post_url:
#    crawler(post_url)
post_id,  = crawler('http://www.chictopia.com/photo/show/1154261-Public+Desire+ankle+boots-black-nasty-gal-top-dark-green-public-desire-boots')

print(a)