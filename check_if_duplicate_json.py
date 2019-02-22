import json
import requests
'''
with open('./combined_woman.json') as infile:
    ds = json.load(infile)

    new_ds = ({elem["post_id"]:elem for elem in ds}.values())
    
with open('./combined_woman_without_duplicate.json', 'w') as outfile:
    json.dump(list(new_ds), outfile, indent=2)


'''  
#with open('./combined_woman_without_duplicate.json', 'r') as infile:
with open('./sample.json', 'r') as infile:
    ds = json.load(infile)
    lst_img_url = ''
    for obj in ds:

        lst_img_url += ','+(json.dumps(obj['img_url']))

    lst_img_url = lst_img_url[1:]
    lst_img_url = lst_img_url.replace('[', '')
    lst_img_url = lst_img_url.replace(']', '')
    lst_img_url = lst_img_url.replace('"', '')
    lst_img_url  = (lst_img_url).split(',')


    for img_url in lst_img_url:

        img_id = img_url.split('/')
        img_id = (img_id[-2]+'_'+img_id[-1])

        with open('./img/'+img_id+'.jpg', 'ab') as f:
            f.write(requests.get(img_url).content)




