import json
import requests
'''
with open('./combined_woman.json') as infile:
    ds = json.load(infile)

    #print({elem["post_id"]:elem for elem in ds}.values())
    new_ds = ({elem["post_id"]:elem for elem in ds}.values())
    #new_ds = new_ds.replace('"post_id"', '\n'+'"post_id"')
    
with open('./combined_woman_without_duplicate.json', 'w') as outfile:
    json.dump(list(new_ds), outfile, indent=2)


'''  
#with open('./combined_woman_without_duplicate.json', 'r') as infile:
with open('./sample.json', 'r') as infile:
    ds = json.load(infile)
    lst_img_url = ''
    for obj in ds:
        #lst_img_url = lst_img_url + list(json.dumps(obj['img_url'][:]))
        #print(type((json.dumps(obj['img_url'][:]))))
        lst_img_url += ','+(json.dumps(obj['img_url']))
    #print(lst_img_url)
    lst_img_url = lst_img_url[1:]
    lst_img_url = lst_img_url.replace('[', '')
    lst_img_url = lst_img_url.replace(']', '')
    lst_img_url = lst_img_url.replace('"', '')
    lst_img_url  = (lst_img_url).split(',')
    #print(lst_img_url)

    for img_url in lst_img_url:
        #img_url = img_url.replace('.jpg', '')
        img_id = img_url.split('/')
        #print(img_id)
        img_id = (img_id[-2]+'_'+img_id[-1])
        print(img_id)
        with open('./img/'+img_id+'.jpg', 'ab') as f:
            f.write(requests.get(img_url).content)




