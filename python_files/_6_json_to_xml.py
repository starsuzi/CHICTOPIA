import json

def extract_basic(img_url, post):

    img_id = img_url.split('/')
    img_id = (img_id[-2]+'_'+img_id[-1][:-8]+'.jpg')
    tags = " ".join(str(tag) for tag in post['tag'])

    return """<?xml version="1.0" encoding="utf-8"?>
<annotation>
  <folder></folder>
  <filename>{}</filename>
  <source>
    <database>http://www.chictopia.com/</database>
    <annotation>{}</annotation>
    <image>{}</image>
    <flickrid>{}</flickrid> 
  </source>
  <owner>
    <flickrid></flickrid>
    <name></name>
  </owner>    
  <size>
    <width></width>
    <height></height>
    <depth>3</depth>
  </size>
  <segmented></segmented>
""".format(
        img_id
        ,tags
        ,post['post_url']
        ,img_url
    )

def extract_object(season, obj, category, colors, sleeves, pattern, gender):
      return """
  <object>
    <name>{}</name>
    <pose></pose>
    <truncated></truncated>
    <difficult></difficult>
    <bndbox>
      <xmin></xmin>
      <ymin></ymin>
      <xmax></xmax>
      <ymax></ymax>
    </bndbox>
    <attributes>
        <colors>{}</colors>
        <gender>{}</gender>
        <season>{}</season>
        <sleeves>{}</sleeves>
        <pattern>{}</pattern> 
        <leg_pose></leg_pose>
        <glasses></glasses>
    </attributes>
  </object>""".format(
              category, colors, season, gender, sleeves, pattern
    )

def check_season(tag):
      
      if 'spring' in tag:
            return 'spring'
      elif 'Spring' in tag:
            return 'spring'
      elif 'summer' in tag:
            return 'summer' 
      elif 'Summer' in tag:
            return 'summer' 
      elif 'fall' in tag:
            return 'fall'  
      elif 'Fall' in tag:
            return 'fall'
      elif 'autumn' in tag:
            return 'fall'
      elif 'Autumn' in tag:
            return 'fall' 
      elif 'winter' in tag:
            return 'winter'      
      elif 'Winter' in tag:
            return 'winter'
      else:
            return ''

def check_category(category):
      
      if category in ['coat']:
            return 'coat'
      elif category in ['dress']:
            return 'dress'
      elif category in ['vest' ]:
            return 'vest'
      elif category in ['shirt', 'blouse', 't-shirt', 'sweater', 'top']:
            return 'shirt'
      elif category in ['jumper']:
            return 'jumper'
      elif category in ['jacket', 'blazer']:
            return 'jacket'
      elif category in ['pants', 'jeans', 'shorts', 'panties', 'leggings']:
            return 'pants'
      elif category in ['skirt']:
            return 'skirt'
      elif category in ['scarf']:
            return 'scarf'
      elif category in ['bag', 'purse']:
            return 'bag'
      elif category in ['shoes', 'sneakers', 'boots', 'flats', 'wedges', 'sandals', 'loafers', 'clogs']:
            return 'shoes'
      elif category in ['hat']:
            return 'hat'
      else:
            return 'None'

def check_color(obj):
      if 'white' in obj:
            return 'white'
      elif 'black' in obj:
            return 'black'
      elif 'gray' in obj:
            return 'gray'
      elif 'pink' in obj:
            return 'pink'
      elif 'red' in obj:
            return 'red'
      elif 'green' in obj:
            return 'green'
      elif 'blue' in obj:
            return 'blue'
      elif 'brown' in obj:
            return 'brown'
      elif 'navy' in obj:
            return 'navy'
      elif 'beige' in obj:
            return 'beige' 
      elif 'yellow' in obj:
            return 'yellow'
      elif 'purple' in obj:
            return 'purple'
      elif 'orange' in obj:
            return 'orange'  
      else:
        return ''           

def check_sleeves(obj):
      if 'short sleeve' in obj:
            return 'short sleeves'
      elif 'long sleeve' in obj:
            return 'long sleeves'
      elif 'longsleeve' in obj:
            return 'long sleeves'
      elif 'no sleeve' in obj:
            return 'no sleeves'
      elif 'sleeveless' in obj:
            return 'no sleeves'
      elif 'maxi skirt' in obj:
            return 'long' 
      elif 'shorts' in obj:
            return 'short' 
      else :
            return ''

def check_pattern(obj):
      if 'check' in obj:
            return 'checker'
      elif 'dot' in obj:
            return 'dotted'
      elif 'floral' in obj:
            return 'floral'
      elif 'flower' in obj:
            return 'floral'
      elif  'rose' in obj:
            return 'floral'
      elif 'daisy' in obj:
            return 'floral'                                
      elif 'stripe' in obj:
            return 'striped'
      else:
            return ''

def convert_to_xml(in_path, out_folder, gender):

      #with open('./man_final.json', 'r') as infile:
      with open(in_path, 'r') as infile:

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

                              item_result += extract_object(season, obj, category, colors, sleeves, pattern, gender)

                        xml_result = img_result+item_result+'\n'+'</annotation>'
                        lst_xml_result.append(xml_result)

      for i, xml_file in enumerate(lst_xml_result):
            out_path = out_folder+lst_file_name[i]+'.xml'
            with open(out_path, 'w') as outfile:
                  outfile.write(xml_file) 

convert_to_xml('./crawling_result/final/woman_final.json', './woman/img/', 'woman')
convert_to_xml('./crawling_result/final/man_final.json', './man/img/', 'man')