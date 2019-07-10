#!/bin/bash/env python

import requests
import urllib.request
from bs4 import BeautifulSoup as bs
import mysql.connector
"""
mydb = mysql.connector.connect(
	host='localhost',
	user='root',
	passwd=''
)
"""
#print(mydb)

def parse_page(url):
	try:
		r = requests.get(url)
		soup = bs(r.text, 'html.parser')
		return soup
	except:
		pass

# returns a list of all models of one brand
def get_models(brand):
	brand = (brand.replace(' ', '-')).lower()
	url ='https://www.polovniautomobili.com/auto-oglasi/pretraga?brand=' + brand
	soup = parse_page(url)
	models= soup.find(id='model')
	models_list=[]
	for model in models:
		models_list.append(model.get_text())
	return models_list[1:]


# returns a list of all brands 
def all_Brands():
	url = 'https://www.polovniautomobili.com/#'
	soup = parse_page(url)
	brands = soup.find(id='brand')
	brands_list = []
	for brand in brands:
		brands_list.append(brand.get_text())

	return brands_list[1:]


# get all cars from one brand and model
def get_cars(brand, model):

	brand = (brand.replace(' ', '-')).lower()
	model = (model.replace(' ', '-')).lower()
	url ='https://www.polovniautomobili.com/auto-oglasi/pretraga?brand=' + brand + '&model[]=' + model

	#soup = parse_page(url)
	"""
	for i in range(1,20):
		soup = parse_page(url+'&page='+i)
		pages = soup.findAll('article')

		for page in pages:
			try:
				link = page.find('h2')

	"""
	soup = parse_page(url)
	pages = soup.findAll('article')
	#title = soup.findAll(class_="ga-title")
	"""
	for t in title:
		t = t.get('title')
		print(t)
	"""
	for page in pages:
		#print(page)
		print("")
		pageT = page.find('a')
		#print(pageT)

		title = pageT.get('title')
		print(title)
		
		discount = page.find(class_='price price-discount')
		#print(discount.get_text())
		if discount!=None:
			pass
			print(discount.get_text())
		else:
			price = page.find(class_='price')
			print(price.get_text())
		content = page.findAll(class_='inline-block')
		for con in content:
			print(con.get_text())

	
	#print(content)


get_cars('Alfa Romeo','75')


#brands = all_Brands()
"""
for brand in brands:
	print(brand)
	print(get_models(brand))
"""
