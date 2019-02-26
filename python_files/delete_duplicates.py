import json
import requests

#delete duplicates
def delete_dulplicates(json_to_check, json_to_save):

    with open(json_to_check) as infile:
        ds = json.load(infile)
        new_ds = ({elem["post_id"]:elem for elem in ds}.values())
    with open(json_to_save, 'w') as outfile:
        json.dump(list(new_ds), outfile, indent=2)

#category_combined_woman.json is the total category combined file 
#delete_dulplicates('./category_combined_woman.json', './result_woman_final.json')