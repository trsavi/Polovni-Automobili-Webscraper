#!/bin/bash/env python

import requests
import urllib.request
from bs4 import BeautifulSoup as bs
import mysql.connector


# function that creates database on local server
def createDB():

	mydb = mysql.connector.connect(
		host='localhost',
		user='root',
		passwd=''
	)
	#database='testDB'

	mycursor = mydb.cursor()

	mycursor.execute("CREATE DATABASE polovniAutomobili")

	# check if database exists
	#mycursor.execute("SHOW DATABASES")
	#for db in mycursor:
	#	print(db)


# parse through page using BeautifulSoup
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
		if model.get_text()=='Ostalo':
			pass
		else:
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

# function that replaces characters in string
def replace(string):
	string = string.replace('š','s')
	string = string.replace('Š','s')
	string = string.replace('ć','c')
	string = string.replace('Ć','c')
	string = string.replace('Ž','z')
	string = string.replace('ž','z')
	string = string.replace('č','c')
	string = string.replace('Č','c')
	return string

# get all cars from one brand and model
def get_cars(brand, model):

	brand = (brand.replace(' ', '-')).lower()
	model = (model.replace(' ', '-')).lower()
	url ='https://www.polovniautomobili.com/auto-oglasi/pretraga?brand=' + brand + '&model[]=' + model

	#soup = parse_page(url)
	carList = []
	# loop over number of pages
	for i in range(1,2):
		#print('page='+str(i))
		#print("")
		soup = parse_page(url+'&page='+str(i))
		#print(soup)
		if soup!=None:

			pages = soup.findAll('article')
			for page in pages:
					#print(page)
				pageT = page.find('a')
				try:
					title = pageT.get('title')
					link = pageT.get('href')
					if title==None:
						pass
					else:
						#print(title)
						discount = page.find(class_='price price-discount')
						if discount!=None:
							price = discount.get_text()
							continue
						else:
							price = page.find(class_='price')
							price = price.get_text()
						content = page.findAll(class_='inline-block')
						blocks = []
						for con in content:
							blocks.append(con.get_text())
						god = int(blocks[0][:4])
						km = blocks[1].replace('.','')
						km = km.replace(' km |', '')
						km = int(km)
						gor = str(blocks[2][:-2])
						gor = replace(gor)
						kub = int(blocks[3][:4])
						kar = (blocks[4].replace(',',''))
						kar = replace(kar)
						sn = (blocks[5].replace(', ',''))

						try:
							price = int(price[:-2].replace('.',''))
							dictionary = {
									'Brend': (brand.replace('-', ' ')).upper(),
									'Model': (model.replace('-', ' ')).upper(),
									'Naziv': replace(title),
									'Cena': price,
									'Godiste': god,
									'Kilometraza':km,
									'Gorivo':gor,
									'Kubikaza':kub,
									'Karoserija':kar,
									'Snaga': sn,
									'Link': link
							}
							# append every car to list as dictionary
							carList.append(dictionary)

						except:
							pass

				except Exception as e: 
					print(e)
					pass
	return carList


# function that inserts cars into database
def insertDBAll():
	mydb = mysql.connector.connect(
		host="localhost",
		user="root",
		passwd="",
		database="polovniAutomobili"
	)

	mycursor = mydb.cursor()

	drop = 'DROP TABLE Cars'

	mycursor.execute(drop)

	mycursor.execute("CREATE TABLE Cars (brend VARCHAR(255), model VARCHAR(255), naziv VARCHAR(255), cena INT(10), godiste INT(10), kilometraza INT(10), gorivo VARCHAR(255), kubikaza INT(10), karoserija VARCHAR(255) ,snaga VARCHAR(255))")

	sqlInsert = "INSERT INTO Cars (brend, model, naziv, cena, godiste, kilometraza, gorivo, kubikaza, karoserija, snaga) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

	# insert cars by brand and model
	brands = all_Brands()
	try:
		for brand in brands:
			models = get_models(brand)

			for model in models:
				if model==None:
					pass
				else:

					cars = get_cars(brand, model)

					for car in cars:
						if car==None:
							pass
						else:
							values = tuple(car.values())
							try:

								mycursor.execute(sqlInsert, values)
								mydb.commit()
							except:
								pass

	except Exception as e:
		#print(values)
		print(e)
		pass

# create database and then insert data
#createDB()
insertDBAll()
print("Data inserted")
