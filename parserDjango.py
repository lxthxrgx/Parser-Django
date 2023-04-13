from openpyxl import *
import sqlite3 as sq
import json
import requests
import re
import random
from collections import OrderedDict
from termcolor import colored
import io
import time
import concurrent.futures as cf
import psycopg2

start_time = time.time()

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

    proxy_url = 'https://advanced.name/freeproxy/64385973911c6' # free proxy
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
    print(colored( 'Proxy: ', 'green' ),tested_proxies, colored("\u2714",'green'), '\n')
    tested_proxies = dict(tested_proxies)
    return tested_proxies
    
wbook = load_workbook(r'F:\Prog\Py\excel\excel sources\parcels.xlsx')
sheet = wbook['parcels']

proxy_dict = proxy_protocol_test()

headers_func = headers()

database = sq.connect('ltx.db')
cursor = database.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS django(
	"id"	TEXT,
	"cadnum"	TEXT,
	"category"	TEXT,
	"area"	TEXT,
	"unit_area"	TEXT,
	"koatuu"	TEXT,
	"use"	TEXT,
	"purpose"	TEXT,
	"purpose_code"	TEXT,
	"ownership"	TEXT,
	"ownershipcode"	TEXT,
	"geometry"	TEXT,
	"address"	TEXT,
	"valuation_value"	TEXT,
	"valuation_date"	TEXT
)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS django_test(
	"id"	TEXT,
	"cadnum"	TEXT,
	"category"	TEXT,
	"area"	TEXT,
	"unit_area"	TEXT,
	"koatuu"	TEXT,
	"use"	TEXT,
	"purpose"	TEXT,
	"purpose_code"	TEXT,
	"ownership"	TEXT,
	"ownershipcode"	TEXT,
	"geometry"	TEXT,
	"address"	TEXT,
	"valuation_value"	TEXT,
	"valuation_date"	TEXT
)''')
cursor.execute('DELETE FROM django')


count_cells = 0
count_requests = 0


def process_cell(cell_value):
    global count_requests
    url = url = 'https://kadastr.live/api/parcels/' + cell_value + '/history/?format=json'
    response = requests.get(url, proxies=proxy_dict, headers=headers_func)
    count_requests += 1
    if response.status_code == 200:
        data = response.json()
        data_str = json.dumps(data)
        data_filtered_str = data_str.replace('""', r'\"\"')
        data_filtered = None
        try:
            data_filtered = json.loads(data_filtered_str)
        except json.decoder.JSONDecodeError as a:
            url_error = url
            f_o = io.open(r'F:\Prog\Py\practice\Parser\url.txt', mode='a')
            f_o.write(str(a) + ': ' + url_error + '\n')
            f_o.close()
        return data_filtered
    else:
        print('Ошибка получения JSON-данных:', response.status_code, url)
    wbook.close()

with cf.ThreadPoolExecutor(max_workers=10) as executor:
    futures = []
    for row in sheet.iter_rows(min_col=1, max_col=1):
        for cell in row:
            count_cells += 1
            futures.append(executor.submit(process_cell, cell.value))
    for future in cf.as_completed(futures):
        data_filtered = future.result()
        if data_filtered is not None:
            cursor.execute('''INSERT INTO django(
            id,
            cadnum,
            category,
            area,
            unit_area,
            koatuu,
            use,
            purpose,
            purpose_code,
            ownership,
            ownershipcode,
            geometry,
            address,
            valuation_value,
            valuation_date)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', 
            ( data_filtered['id'], data_filtered['cadnum'], data_filtered['category'], data_filtered['area'], data_filtered['unit_area'], data_filtered['koatuu'], data_filtered['use'], data_filtered['purpose'], data_filtered['purpose_code'], data_filtered['ownership'], data_filtered['ownershipcode'], json.dumps(data_filtered['geometry']), data_filtered['address'], data_filtered['valuation_value'], data_filtered['valuation_date']))
print("Количество ячеек:", count_cells)
print("Количество запросов:", count_requests)
#print("Количество запросов 2: ", count_requests1)


print('--------------')
print(colored('Header: ','green'),headers())
print('--------------')
print(colored('Random Proxy: ','green'),proxy_random())
print('--------------')
proxy_file_dict = {}
wbook.close()
def proxy_file_error():
    
    with io.open(r'practice\Parser\url.txt') as f:
        for line in f:
            urls_txt = re.findall("(?P<url>https?://[^\s]+)", line)
            for url_txt in urls_txt:
                proxy_file_dict[url_txt] = None
                #print(url_txt)
    # здесь может быть какой-то дополнительный код

    print(proxy_file_dict)
    print('Len: ',colored(len(proxy_file_dict), 'green'))

    values_set = set(proxy_file_dict.values())
    if len(values_set) == len(proxy_file_dict.values()):
        print(colored("No repeated values", 'green' ))
    else:
        print(colored ( "There are repeated values", 'red'))

    for url in proxy_file_dict:
        try:
            response = requests.get(url)
            response_json = json.loads(response.text)
            
        except Exception as json_error:
            print(colored( 'Error: ', 'red'),{json_error}, 'Url: ', colored({url},'red'))
        print(response_json)
        cursor.execute('''INSERT INTO django_test(
            id,
            cadnum,
            category,
            area,
            unit_area,
            koatuu,
            use,
            purpose,
            purpose_code,
            ownership,
            ownershipcode,
            geometry,
            address,
            valuation_value,
            valuation_date)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', 
            ( response_json['id'], response_json['cadnum'], response_json['category'], response_json['area'], response_json['unit_area'], response_json['koatuu'], response_json['use'], response_json['purpose'], response_json['purpose_code'], response_json['ownership'], response_json['ownershipcode'], json.dumps(response_json['geometry']), response_json['address'], response_json['valuation_value'], response_json['valuation_date']))

    f.close()            
    return response_json
proxy_file_error()
#cursor.execute('DELETE FROM django')

cursor.execute('SELECT COUNT(*) FROM django_test')
django_test = cursor.fetchall()[0]

cursor.execute('SELECT COUNT(*) FROM django')
django = cursor.fetchall()[0]
duplicate_rows = set(django_test).intersection(django)

if len(duplicate_rows) > 0:
    print(colored('There are duplicate rows between django_test and django', 'red'))
    print(colored('Duplicate rows:', 'red'), duplicate_rows)
    print(colored('Data inserted successfully', 'green'))
else:
    print(colored('There are no duplicate rows between django_test and django', 'green'))
    cursor.execute('''INSERT INTO django(
    id,
	cadnum,
	category,
	area,
	unit_area,
	koatuu,
	use,
	purpose,
	purpose_code,
	ownership,
	ownershipcode,
	geometry,
	address,
	valuation_value,
	valuation_date
    ) 
    SELECT 
    id,
	cadnum,
	category,
	area,
	unit_area,
	koatuu,
	use,
	purpose,
	purpose_code,
	ownership,
	ownershipcode,
	geometry,
	address,
	valuation_value,
	valuation_date
    FROM django_test
    ''')
database.commit()
database.close()
end_time = time.time()
total_time = end_time - start_time
print("Время выполнения кода:", total_time/60, "минут")


