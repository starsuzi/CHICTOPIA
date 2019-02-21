import json

with open('./combined_woman.json') as infile:
    ds = json.load(infile)

    #print({elem["post_id"]:elem for elem in ds}.values())
    new_ds = {elem["post_id"]:elem for elem in ds}.values()
    #new_ds = new_ds.replace('"post_id"', '\n'+'"post_id"')

with open('./combined_woman_without_duplicate.json', 'w') as outfile:
    json.dump(list(new_ds), outfile)