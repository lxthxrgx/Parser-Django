from openpyxl import * 
import sqlite3 as sq
import json
import requests

wbook = load_workbook(r'excel\excel sources\parcels.xlsx')
sheet = wbook['parcels']
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
				except json.decoder.JSONDecodeError:
					print('Ошибка декодирования JSON-данных:', url) 
		else:
			a_null = print('Ошибка получения JSON-данных:', response.status_code,url)
						

print(len(url))

wbook.close()
database.commit()
database.close()
