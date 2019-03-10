import json
import requests

def image_downloader(in_path, out_folder): 
    
    with open(in_path, 'r') as infile:
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
            img_id = (img_id[-2]+'_'+img_id[-1][:-8])

            with open(out_folder+img_id+'.jpg', 'ab') as outfile:
                outfile.write(requests.get(img_url).content)

#image_downloader('./crawling_result/final/man_final.json', './man/img/')
image_downloader('./crawling_result/final/woman_final.json', './woman/img/')




