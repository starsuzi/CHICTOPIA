with open('./man_final.json', 'r') as infile:

    ds = json.load(infile)

    lst_xml_result = []
    lst_file_name = []

    for post in ds:
        tag = str(post['tag'])

        for img_url in post['img_url']:
            img_result = extract_basic(img_url, post)
            img_id = img_url.split('/')
            img_id = (img_id[-2]+'_'+img_id[-1][:-8])
            lst_file_name.append(img_id)

            item_result = ""
            for obj in post['item']:
                  
                category = check_category(''.join(obj.split(" ")[-1:]))

                season = ''
                colors = ''
                sleeves = ''
                pattern = ''

                if category == 'None':
                      continue

                colors = check_color(obj)
                
                if category in ['coat', 'dress','vest', 'shirt', 'jumper', 'jacket', 'pants','skirt']:
                    
                    sleeves = check_sleeves(obj)             
                    pattern = check_pattern(obj)             
                    season = check_season(tag)

                item_result += extract_object(season, obj, category, colors, sleeves, pattern)

            xml_result = img_result+item_result+'\n'+'</annotation>'
            lst_xml_result.append(xml_result)

for i, xml_file in enumerate(lst_xml_result):
  #with open('./woman_xml/'+lst_file_name[i]+'.xml', 'w') as outfile:
  with open('./man_xml/'+lst_file_name[i]+'.xml', 'w') as outfile:
    outfile.write(xml_file) 