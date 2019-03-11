import crawling_module
from multiprocessing import Pool, Manager

#main
if __name__ == '__main__':

    lst_page_url_man = ['http://www.chictopia.com/browse/people?g=2'] # list for page url
    nested_nested_result = []
    flat_result = []
    
    #total 936 pages 
    for i in range(2, 936):#936
        lst_page_url_man.append(crawling_module.get_next_page_man(i,''))

    p = Pool(16)
    res = p.map(crawling_module.get_post, lst_page_url_man)

    if res is not None:
        nested_nested_result.append(res)

    for nested_sublist in nested_nested_result:
        for sublist in nested_sublist:
            for item in sublist:
                flat_result.append(item)

    with open("./crawling_result/text/result_man.txt", "w") as output:
        output.write(str(set(flat_result)))
    
    crawling_module.text_to_json('man')

