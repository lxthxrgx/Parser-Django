from openpyxl import * 
import sqlite3 as sq
import json
import requests

wbook = load_workbook(r'excel\excel sources\parcels.xlsx')
sheet = wbook['parcels']

for row in sheet.iter_rows(min_col=1, max_col=1):
    for cell in row:
        url = 'https://kadastr.live/api/parcels/'+cell.value+'/history/?format=json'
        response = requests.get(url)
        if (response.status_code == 200):
            data = response.text.replace('""', r'\"\"')
            b = json.loads(data)
            a = b['id'], b['cadnum'], b['category'], b['area'], b['unit_area'], b['koatuu'], b['use'], b['purpose'], b['purpose_code'], b['ownership'], b['ownershipcode'], b['geometry'], b['address'], b['valuation_value'], b['valuation_date']
        else:
            print('Ошибка получения JSON-данных:', response.status_code,url)

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

cursor.execute('''INSERT INTO django(Cudnum,
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
 VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',(b['id'], b['cadnum'], b['category'], b['area'], b['unit_area'], b['koatuu'], b['use'], b['purpose'], b['purpose_code'], b['ownership'], b['ownershipcode'], b['geometry'], b['address'], b['valuation_value'], b['valuation_date']))