# %%
import re
import requests
import pandas as pd
import time
from lxml import etree
import os
from random import randint
import json
from tqdm import tqdm

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
df_output = pd.DataFrame()

kraj = 'pl'
# df_total_all_cat = pd.DataFrame()
# base_url = 'https://products.dm.de/product/cz/search'


###AKTUALNY, DO TESTOW KOMENTARZ --> base_url = 'https://product-search.services.dmtech.com/cz/search/static'

base_url = 'https://product-search.services.dmtech.com/' + kraj + '/search/static'

category_url = 'https://product-search.services.dmtech.com/' + kraj + '/search?query=%3F&searchType=category'
category_j = requests.get(category_url, headers=header).json()
kategorie = []
kat_dict = {'kategorie': kategorie}

for i in range(0, len(category_j.get('facets')[0].get('values'))):
    kategorie.append(category_j.get('facets')[0].get('values')[i].get('name'))

# kat_list = list(kat_dict.values())
### SPROBOWAC SZUKAC PO KATEGORIACH
# 'https://product-search.services.dmtech.com/cz/search?query=%3F&searchType=product&categoryNames=P%C3%A9%C4%8De%20o%20t%C4%9Blo&totalPages=5&sort=rating&currentPage=20&type=search'
### DODAC PARAMETR MOWIACY O TYM W JAKIEJ AKTUALNIE JESTESMY KATEGORII - JEST LIMIT DO 1000 SZTUK PRZY ZAPYTANIU NA TOTALA

# %%
dane_jj = []

# rynki = ['cz', 'de', 'hu', 'sk', 'hk', 'at']
# output = [{}] # zeby latwo zrobić append


########################## DEMO SZUKANIA PO KATEGORIACH:

# for i in range(0,10): print(dane_j.get('facets')[0].get('values')[i].get('name'))
# https://product-search.services.dmtech.com/cz/search?query=%3F&categoryNames=P%C3%A9%C4%8De%20o%20t%C4%9Blo&currentPage=0 ^^^ to powyższe
# ^^^^ i to zostaje naszym base url po ktorym sie poruszamy zmieniajac strony
# = 'https://product-search.services.dmtech.com/cz/search?query=%3F&searchType=category'
# NA CZECHACH MAMY AZ 200 KATEGORII
##########################

# TODO cz sk hu  at de hk
# lista linków kategorii
#     //*[@id="app"]/div/header/div[3]/div/div/ul[@data-dmid="desktop-navigation-items"]/li[*]/a/@href

# url = 'https://products.dm.de/product/cz/search?productQuery=%3Anew%3Arelevance%3AallCategories&currentPage=1&purchasableOnly=false&hideFacets=false&hideSorts=false&pageSize=100
# https://product-search.services.dmtech.com/cz/search


#####
params = {
    # 'productQuery' : ':new:relevance:allCategories',
    # 'productQuery' : '%3Anew%3Arelevance%3AallCategories&',
    # 'facets' : ':values:name:Péče o tělo',
    'currentPage': '0',
    'purchasableOnly': 'false',
    'hideFacets': 'false',
    'hideSorts': 'false',
    'categoryNames': ''
    # 'pageSize' : '30'
}

dane_j = requests.get(base_url, headers=header, params=params).json()
# kategorie trzeba dobrze dopiąc do reszty jako dict w jednej kolumnie
# df_output = df_output.append(kat_list,sort='False',ignore_index=True)

# liczba_stron = dane_j.get("totalPages")
params['pageSize'] = dane_j.get("pageSize")
# kategoria = dane_j.get('facets').get('values')
# %%
for i in tqdm(range(0, len(kategorie))):
    params['categoryNames'] = str(kategorie[i])
    liczba_stron = dane_j.get("totalPages")
    print(str(kategorie[i]))
    for k in tqdm(range(0, liczba_stron)):
       # print(k * (i + 1))
        print(k)
        params['currentPage'] = str(k)

        # print(params['currentPage'])

        # print(str(i)+'/'+str(liczba_stron))
        time.sleep(randint(1, 10))
        dane_j = requests.get(base_url, headers=header, params=params).json()
        dane_jj.append(dane_j)
        # df_output = df_output.append(dane_j.get("products"), sort='False')
        # transpose do usuniecia jak juz ogarne dodawanie dicta do df zeby nie zaburzyc struktury danych
        df_output = df_output.append(dane_j.get("products"), sort='False')

# df_test = pd.DataFrame(dane_j.get("products"))
# df_output['links']=df_output['links'].apply(get_link_df)
# %%

# df_output.hazardSymbols = df_output.hazardSymbols.apply(lambda x : str(x))
# df_output.basePrice = df_output.basePrice.apply(lambda x : str(x))
# df_output.price = df_output.price.apply(lambda x : str(x))
df_output.to_excel('dm_' + kraj + '_test.xls')

# with open ('test.json', 'w') as plik:
#     plik.write(dane_j.dumps)
#     json.dump(dane_j, plik)

# #namiary na pola
# url_xpath = '//div[contains(@class,"product-name")]//@href'
# name_xpath = '//div[contains(@class,"product-name")]//a/text()'
# crossed_price_xpath = '//p[contains(@class,"old-price")]/span/span/text()'
# price_special_xpath = '//p[contains(@class,"special-price")]/span/span/text()'
# price_regular_xpath = '//span[contains(@class,"regular-price")]/span[@class ="price"]/text()'
# producer_xpath = '//div[contains(@class,"product-manufacturer-name")]/span/text()'

# proxies={
#         "http": "http://4e380e22065c458f887d235666f62012:@proxy.crawlera.com:8011/",
#         "https": "https://4e380e22065c458f887d235666f62012:@proxy.crawlera.com:8011/"
#     }

# # page_SKU_dict = {
# #           'gtin' : gtin_list[0],
# #           'url'  : tree.xpath(url_xpath),
# #           'name'  : clean_field(tree.xpath(name_xpath),2),
# #           'crossed_price'  : tree.xpath(crossed_price_xpath),
# #           'price'  : tree.xpath(price_xpath),
# #           'producer'  : tree.xpath(producer_xpath)
# # }


# #"C:\Users\akobus\Documents\Python Scripts\natura_gtin\input.txt"
# def get_gtin(file):
#     with open(file,'r') as plik:
#         lista_gtin = plik.read().split('\n')
#     return lista_gtin

# def return_tree(url):
#     data = requests.get(url,headers=header,  proxies=proxies,
#                  verify=False)
#     data_str = data.text
#     htmlparser = etree.HTMLParser()
#     return etree.fromstring(data_str,htmlparser)

# def clean_field(field, idx):
#     if len(field)>0:
#         field = str(field[idx]).replace('\r','').replace('  ','').replace('\n','')
#         return field
#     pass

# def get_SKU(gtin):
#     url = url_base + gtin
#     tree = return_tree(url)
#     single_SKU_dict = {
#           'gtin' : gtin,
#           'url'  : tree.xpath(url_xpath),
#           'name'  : clean_field(tree.xpath(name_xpath),0),
#           'crossed_price'  : clean_field(tree.xpath(crossed_price_xpath),0),
#           'price_special'  : clean_field(tree.xpath(price_special_xpath),0),
#           'price_regular'  : clean_field(tree.xpath(price_regular_xpath),0),
#           'producer'  : tree.xpath(producer_xpath)
#     }
#     return single_SKU_dict

# #%%
# gtin_list = get_gtin(r"C:\Users\akobus\Documents\Python Scripts\natura_gtin\input.txt")

# gtin_list_list = [gtin_list[i:i + 1000] for i in range(0, len(gtin_list), 1000)]

# for x, gtin_list_partial in enumerate(gtin_list_list):
#     i = len(gtin_list_partial)
#     j = 1

#     for gtin in gtin_list_partial:
#         time.sleep(randint(1,2))
#         try:
#             output_single = get_SKU(gtin)
#         except Exception:
#             print('blad')
#             output={}
#         output.append(output_single)

#         print(str(j) + " / " + str(i))
#         j += 1
#         # if j > 5: break
#         print(gtin)
#         print(output_single)

#     df_total = pd.DataFrame(output)
#     df_total.to_excel('all_data'+str(x)+'.xls')

# # print(output)
# #%%
# # url
# # '/html/body/div[2]/section[2]/div[2]/div[4]/div/div[1]/ul/li/div/div/div[6]/h2/a/@href'

# # nazwa
# # '/html/body/div[2]/section[2]/div[2]/div[4]/div/div[1]/ul/li/div/div/div[6]/h2/a/text()'

# # producent
# # '/html/body/div[2]/section[2]/div[2]/div[4]/div/div[1]/ul/li/div/div/div[4]/span'

# # cena reg
# # '/html/body/div[2]/section[2]/div[2]/div[4]/div/div[1]/ul/li/div/div/div[8]/div/div/p[1]/span/span/text()'

# # cena
# # '/html/body/div[2]/section[2]/div[2]/div[4]/div/div[1]/ul/li/div/div/div[8]/div/div/p[2]/span[2]/span/text()'

# # for x,y in enumerate(gtin_list_list):
# #     print(x,y[0])
