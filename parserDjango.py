from openpyxl import *
import sqlite3 as sq
import json
import requests
import re
import random
from collections import OrderedDict
import random
from termcolor import colored
import io

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
        },Ф
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

    proxy_url = 'https://advanced.name/freeproxy/642e879d4abd3' # free proxy
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
    
wbook = load_workbook(r'excel\excel sources\parcels.xlsx')
sheet = wbook['parcels']

proxy_dict_ = proxy_protocol_test()

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



for row in sheet.iter_rows(min_col=1, max_col=1):
    for cell in row:
        url = 'https://kadastr.live/api/parcels/' + cell.value + '/history/?format=json'
        response = requests.get(url, proxies = proxy_dict_,headers = headers_func)
        wbook.close()
        if (response.status_code == 200):
            data = response.json()
            data_str = json.dumps(data)
            data_filtered_str = data_str.replace('""', r'\"\"')
            try:
                data_filtered = json.loads(data_filtered_str)
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
            except json.decoder.JSONDecodeError as a:
                url_error = url
                f_o = io.open(r'practice\Parser\url.txt', mode='a')
                f_o.write(str(a) + ': ' + url_error + '\n')
                f_o.close()
        else: 
            a_null = print('Ошибка получения JSON-данных:', response.status_code,url)
database.commit()
database.close()


def proxy_file_error():
    proxy_file = io.open(r'practice\Parser\url.txt')
    proxy_file_data = proxy_file.read()
    proxy_file_lines = proxy_file_data.splitlines()

    proxy_file_dict = {}
    for line in proxy_file_lines:
        values = line.split()
        proxy_file_values_list = values[8]
        proxy_file_dict[values[8]] = proxy_file_values_list

        #print(proxy_file_dict)

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
            #print(response_json)
        except Exception as json_error:
            print(colored( 'Error: ', 'red'),{json_error}, 'Url: ', colored({url},'red'))
    proxy_file.close()


    for url in proxy_file_dict:
        try:
            response = requests.get(url)
            if response.ok:
                response_json = response.json()
                print(response_json)
            else:
                print(colored('Error: Response not OK', 'red'), 'Url:', colored(url, 'red'))
        except Exception as json_error:
            print(colored('Error:', 'red'), json_error, 'Url:', colored(url, 'red'))
    return response_json

#cursor.execute('DELETE FROM django')
database = sq.connect('ltx.db')
cursor = database.cursor()

proxy_file = io.open(r'practice\Parser\url.txt')
proxy_file_data = proxy_file.read()
proxy_file_lines = proxy_file_data.splitlines()

proxy_file_dict = {}
for line in proxy_file_lines:
    values = line.split()
    proxy_file_values_list = values[8]
    proxy_file_dict[values[8]] = proxy_file_values_list

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
        response_json_dumps = json.dumps(response_json)
        response_json_filtered = response_json_dumps.replace("''", r"\'\'")
        response_json_filtered = response_json

        class Database_Json:
            id = response_json['id']
            cadnum = response_json['cadnum']
            category = response_json['category']
            area = response_json['area']
            unit_area = response_json['unit_area']
            koatuu = response_json['koatuu']
            use = response_json['use']
            purpose = response_json['purpose']
            purpose_code = response_json['purpose_code']
            ownership = response_json['ownership']
            ownershipcode = response_json['ownershipcode']
            geometry = response_json['geometry']
            address = response_json['address']
            valuation_value = response_json['valuation_value']
            valuation_date = response_json['valuation_date']

            def to_list(self):
                return [self.id, self.cadnum, self.category, self.area, self.unit_area, self.koatuu, self.use, self.purpose, self.purpose_code, self.ownership, self.ownershipcode, json.dumps(self.geometry), self.address, self.valuation_value, self.valuation_date]

        database_json = Database_Json()
        values = database_json.to_list()
        cursor.execute('''INSERT INTO django_test(id,cadnum,category,area,unit_area,koatuu,use,purpose,purpose_code,ownership,ownershipcode,geometry,address,valuation_value,valuation_date) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', values)
        print(colored('Data inserted successfully', 'green'))
        print('django - test: ', cursor.fetchall())
    except Exception as e:
        print(colored('Error inserting data:', 'red'), e)
        database.rollback()

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


