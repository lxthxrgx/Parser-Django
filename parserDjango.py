from openpyxl import * 
import sqlite3 as sq
import json
import requests
import re
import time 
import random

proxy_url = 'https://advanced.name/freeproxy/64286e8f80204'#free proxy

response = requests.get(proxy_url.encode()) 
proxy = response.content.decode()

proxy_filter = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\:\d{1,5}'
proxy_list = re.findall(proxy_filter, proxy)

proxies = {
    'http':[],
    'https':[]
}

for proxy_http in proxy_list:
    proxy_http = ('http://' +  proxy_http)
    proxies['http'].append(proxy_http)

for proxy_https in proxy_list:
    proxy_https = ('https://' + proxy_https)
    proxies['https'].append(proxy_https) 


if len(proxies['http']) > 0:
    proxy_random = random.choice(proxies['http'])
    print('Random http proxy: ', proxy_random)
else:
    print('Список прокси-серверов пуст')

if len(proxies['https']) > 0:
    proxy_random = random.choice(proxies['https'])
    print(proxy_random)
    print('Random https proxy: ', proxy_random)
else:
    print('Список прокси-серверов пуст',)  

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

wbook = load_workbook(r'excel\excel sources\parcels.xlsx')
sheet = wbook['parcels']

for row in sheet.iter_rows(min_col=1, max_col=1):
	for cell in row:
		url = 'https://kadastr.live/api/parcels/'+cell.value+'/history/?format=json'

response = requests.get(url)
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

wbook.close()
database.commit()
database.close()
#{"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
