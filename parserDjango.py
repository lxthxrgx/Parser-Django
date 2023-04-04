from openpyxl import *
import sqlite3 as sq
import json
import requests
import re
import time 
import random
from collections import OrderedDict
import random

def headers():
    headers_list = [  
        # Firefox 77 Mac
        {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://www.google.com/",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        },
        # Firefox 77 Windows
        {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://www.google.com/",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        },
        # Chrome 83 Mac
        {
            "Connection": "keep-alive",
            "DNT": "1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Dest": "document",
            "Referer": "https://www.google.com/",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
        },
        # Chrome 83 Windows 
        {
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Referer": "https://www.google.com/",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9"
        }
    ]   
    ordered_headers_list = []
    for headers in headers_list:
        h = OrderedDict()
        for header,value in headers.items():
            h[header]=value
        ordered_headers_list.append(h)
    for i in range(1,4):
        headers = random.choice(headers_list)
        r = requests.Session()
        r.headers = headers
    headers_dict = dict(headers)
    return headers_dict

def proxy_random():
    proxies_dictionary = { 
        'http':[],
        'https':[]
        }

    proxy_url = 'https://advanced.name/freeproxy/642b39b8b02a7' # free proxy
    response = requests.get(proxy_url)
    proxy = response.content.decode()

    proxy_filter = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\:\d{1,5}'
    proxy_list = re.findall(proxy_filter, proxy)
    for proxy_http in proxy_list:   
        proxy_http = ('http://' +  proxy_http)
        proxies_dictionary['http'].append(proxy_http)

    #print('Proxy http: ',proxies_dictionary['http'])

    for proxy_https in proxy_list:
        proxy_https = ('https://' + proxy_https)
        proxies_dictionary['https'].append(proxy_https)

    #print('Proxy https: ',proxies_dictionary['https'])    

    #print('Proxy dictionary: ',proxies_dictionary)

    if len(proxies_dictionary['http']) > 0:
        proxy_random_http = random.choice(proxies_dictionary['http'])
    else:
        print('Список прокси-серверов http пуст')
        proxy_random_http = None

    if len(proxies_dictionary['https']) > 0:
        proxy_random_https = random.choice(proxies_dictionary['https'])
    else:
        print('Список прокси-серверов https пуст')
        proxy_random_https = None
    return {'http': proxy_random_http, 'https': proxy_random_https}

def proxy_protocol_test():
    tested_proxies = []
    proxy_dict = proxy_random()
    proxy_url_test = 'https://example.com'
    try:
        response = requests.get(proxy_url_test, proxies={'http': proxy_dict['http']})
        if response.status_code == 200:
            tested_proxies.append(proxy_dict)
    except requests.exceptions.RequestException:
        pass
    try:
        response = requests.get(proxy_url_test, proxies={'https': proxy_dict['https']})
        if response.status_code == 200:
            tested_proxies.append(proxy_dict)

    except requests.exceptions.RequestException:
        pass
    print(tested_proxies, "\u2714")
    tested_proxies = dict(tested_proxies)
    return tested_proxies
    
wbook = load_workbook(r'excel\excel sources\parcels.xlsx')
sheet = wbook['parcels']

for row in sheet.iter_rows(min_col=1, max_col=1):
	for cell in row:
		url = 'https://kadastr.live/api/parcels/' + cell.value + '/history/?format=json'
                
print('-------------------')
print(proxy_protocol_test())
print('-------------------')

proxy_dict_ = proxy_protocol_test()

headers_func = headers()

response = requests.get(url, proxies = proxy_dict_,headers = headers_func)

for response_get_json_data in response:
    if (response.status_code == 200):
        data = response.json()
        data_str = json.dumps(data)
        data_filtered_str = data_str.replace('""', r'\"\"')
        try:
             data_filtered = json.loads(data_filtered_str)
        except json.decoder.JSONDecodeError:
            print('Ошибка декодирования JSON-данных:', url) 
    else: 
         a_null = print('Ошибка получения JSON-данных:', response.status_code,url)
print(data_filtered)


