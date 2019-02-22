from dicttoxml import dicttoxml
import json

def convert_to_xml(img_url, post):
    #print(type(post))
    return """<?xml version="1.0" encoding="utf-8"?>
<annotation>
  <folder></folder>
  <filename></filename>
  <source>
    <database></database>
    <annotation></annotation>
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
  <object>
    <name></name>
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
        <colors></colors>
        <gender></gender>
        <season></season>
        <sleeves></sleeves>
        <pattern></pattern>
        <leg_pose></leg_pose>
        <glasses></glasses>
    </attributes>
  </object>
</annotation>""".format(
        post['post_url']
        ,img_url
    )

with open('./sample.json', 'r') as infile:
    ds = json.load(infile)
    #print(ds)
    for post in ds:
        print(post)
        #print(type(post))
        #print(post['post_url'])
        #print(post['img_url'])
        for img_url in post['img_url']:
            result = convert_to_xml(img_url, post)
            print(result)
