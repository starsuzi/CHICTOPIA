import glob

filenames = glob.glob("./crawling_result/json/*.json")
filenames.remove('./crawling_result/json\\result_man.json')

with open('./crawling_result/temp/woman_combined.txt', 'w') as outfile:
    for fname in filenames:
        with open(fname) as infile:
            for line in infile:
                outfile.write(line)

with open('./crawling_result/temp/woman_combined.txt', 'r') as infile:
    filedata = infile.read()
    filedata = filedata.replace(']'+'\n'+'[', ",")

with open('./crawling_result/temp/woman_combined.json', 'w') as outfile:
    outfile.write(filedata)