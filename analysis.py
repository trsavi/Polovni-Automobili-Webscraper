#!/bin/bash/env python

# imports 
import mysql.connector
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import operator

# connect to database
def connectDB():
	
	database = mysql.connector.connect(
		host="localhost",
		user="root",
		passwd="",
		database="polovniAutomobili"
	)

	return database


mydb = connectDB()
mycursor = mydb.cursor()
	
# Comparisson between bmw, audi and volvo
# PROBLEM 1
def comparisonBAV():
	# Making queries
	bmw = "SELECT kilometraza, cena from Cars WHERE brend='bmw' AND model='x3' ORDER BY kilometraza"
	audi = "SELECT kilometraza, cena from Cars WHERE brend='audi' AND model='q5' ORDER BY kilometraza"
	volvo = "SELECT kilometraza, cena from Cars WHERE brend='volvo' AND model='xc60' ORDER BY kilometraza"

	mycursor.execute(bmw)
	bmw_data = mycursor.fetchall()
	
	mycursor.execute(audi)
	audi_data = mycursor.fetchall()

	mycursor.execute(volvo)
	volvo_data = mycursor.fetchall()

	mycursor.close()
	# BMW
	km_bmw = []
	price_bmw = []
	for items in bmw_data:
		km_bmw.append(items[0])
		price_bmw.append(items[1])

	# AUDI
	km_audi = []
	price_audi = []
	for items in audi_data:
		km_audi.append(items[0])
		price_audi.append(items[1])

	# VOLVO

	km_volvo = []
	price_volvo = []
	for items in volvo_data:
		km_volvo.append(items[0])
		price_volvo.append(items[1])
	plt.plot(km_bmw,price_bmw, 'r', label='BMW')
	plt.plot(km_volvo, price_volvo, 'g', label='Volvo')
	plt.plot(km_audi, price_audi, 'b',label='Audi')
	plt.xlabel("Mileage in km")
	plt.ylabel("Price in euros")
	plt.title("Comparison between BMW X3, Audi Q5 and Volvo XC60")
	plt.legend()
	plt.show()

# visualizing comparisson of strongest SUVs currently on website by average value in HP
# PROBLEM 2

def strongestSUV():

	query = "SELECT DISTINCT brend, model, godiste, snaga FROM Cars WHERE (godiste>=2010 AND godiste<=2019 AND karoserija='Dzip/SUV') "
	mycursor.execute(query)
	data = mycursor.fetchall()
	np.set_printoptions(threshold= np.inf)
	data = np.asarray(data)

	
	for snaga in data:
		#snaga[4] = (snaga(4).split(' '))
		snaga[3] = int((snaga[3]).split(' ')[0][:-2])
		#dataA.append(snaga)
	
	# extract brands from all the cars in list
	data = list(data)
	seen = set()
	result = []
	for item in data:
		if item[0] not in seen:
			seen.add(item[0])
			result.append(item[0])
	
	avg = []
	count = 0
	sum1 = 0
	it = 0

	# calculate average in kWh
	for brend in result:
		for i in range(0,len(data)+1): 
				if(it<len(data)):

					if brend==data[it][0]:
						sum1 += int(data[it][3])
						count += 1
						
						
						it+=1
						
						
					else:
						avg.append(sum1/count)
						
						sum1 = 0
						count = 0
						break
				else:
					avg.append(sum1/count)
					break

	#print(data)

	dictionary = dict(zip(result,avg))
	
	sorted_x = sorted(dictionary.items(), key=operator.itemgetter(1))

	x, y = zip(*sorted_x)
	plot = plt.figure(figsize=(15,7))
	plt.bar(x, y, alpha=0.7)
	plt.ylabel('Average power in kW')
	plt.xlabel('Brand')
	plt.title("Comparison of average power of SUV car brand in the last decade")
	plt.xticks(rotation=60)
	plt.tick_params(axis='x', which='major', labelsize=7)
	
	plt.show()


# PROBLEM 3
def countCars():

	query = "SELECT brend, COUNT(*) FROM Cars WHERE godiste>2018 GROUP BY brend HAVING COUNT(*)>20"
	mycursor.execute(query)
	data = mycursor.fetchall()

	dictionary = dict(data)

	sorted_x = sorted(dictionary.items(), key=operator.itemgetter(1))

	x, y = zip(*sorted_x)
	#plt.figure(figsize=(7,12))
	
	# plt.barh(x,y, align='center', color= 'g')
	plt.pie(y, labels=x,autopct='%1.2f%%', shadow=True, startangle=140)
	plt.title("Number (>20) of used cars from 2018 until now")
	plt.tick_params(axis='y', which='major', labelsize=7)
	plt.show()




	
def convert(brand):
	brand = np.asarray(brand)
	for item in brand:
		try:
			item[1] = int((item[1]).split(' ')[0][:-2])
			
		except:
			pass
	return brand

# PROBLEM 4

def oldestCars():

	averageYears = "SELECT brend, AVG(godiste) FROM Cars GROUP BY brend"
	mycursor.execute(averageYears)
	data = mycursor.fetchall()
	data = np.asarray(data)

	dictionary = dict(data)

	sorted_x = sorted(dictionary.items(), key=operator.itemgetter(1))

	x, y = zip(*sorted_x)
	plt.figure(figsize=(15,5))
	plt.bar(x,y,  color='g')
	plt.xlabel('Brand')
	plt.xticks(rotation=60)
	plt.tick_params(axis='x', which='major', labelsize=7)
	plt.title("Average age of used cars")
	plt.ylabel('Average age')
	plt.ylim((1970,2020))
	plt.show()
	

# PROBLEM 5

def mostExpensive(price1,price2):

	
	mycursor.execute("SELECT brend, AVG(cena) FROM Cars WHERE cena<%s and cena>%s GROUP BY brend", (price2,price1))
	data = mycursor.fetchall()
	data = np.asarray(data)

	dictionary = dict(data)

	sorted_x = sorted(dictionary.items(), key=operator.itemgetter(1))

	x, y = zip(*sorted_x)
	plt.figure(figsize=(15,5))
	plt.bar(x,y,  color='g')
	plt.xlabel('Brand')
	plt.xticks(rotation=60)
	plt.tick_params(axis='x', which='major', labelsize=7)
	plt.title("Average price for cars between price %s and %s" %(price1,price2))
	plt.ylabel('Average price')
	plt.ylim((price1,price2))
	plt.show()

# PROBLEM 6
	
def compareSpecs():

	
	plt.figure(figsize=(12,6))
	result = ['Audi','Bmw','Mercedes Benz', 'Volvo','Nissan','Toyota','Seat','Skoda']
	for brend in result:
		array = dict()

		for step in range(50000,250000,10000):

			mycursor.execute("SELECT AVG(kilometraza), AVG(cena) FROM Cars WHERE (brend=%s and kilometraza>%s and kilometraza<%s+10000)", (str(brend),step,step))

			data = mycursor.fetchall()
			data = np.asarray(data)
			#print(data[0][0])

			
			try:
				array[data[0][0]] = data[0][1]
				#print(array)
			except:
				pass
		
		
		for i in list(array):
			if i is None:
				del array[i]
	
		
		try:
			sorted_x = sorted(array.items(), key=operator.itemgetter(0))
			x, y = zip(*sorted_x)
			plt.plot(x,y,label='%s' %brend)

		except:
			continue
	
	plt.legend()
	plt.title("Average price for average mileage in range 50000km - 200000km")
	plt.xlabel('Average Mileage')
	plt.ylabel('Average Price in Euros')	
	plt.show()

# PROBLEM 7

def strongestCars():

	mycursor.execute("SELECT brend FROM Cars GROUP BY brend")
	brendovi = mycursor.fetchall()
	brendovi = list(brendovi)

	array =  dict()
	for x in brendovi:
	
		mycursor.execute("SELECT model, AVG(snaga) as asnaga from Cars WHERE brend=%s GROUP BY model ORDER BY asnaga DESC LIMIT 1", (x[0],))
		data = mycursor.fetchall()
		data = np.asarray(data)
		array[data[0][0]] = float(data[0][1])
	
	sorted_x = sorted(array.items(), key=operator.itemgetter(1))
	width = 0.4
	x, y = zip(*sorted_x)

	
	plt.figure(figsize=(7,10))
	plt.xlabel('Average power per model')
	plt.ylabel('Models')
	#plt.xticks(rotation=50)
	plt.tick_params(axis='y', which='major', labelsize=7)
	plt.barh(x,y,width,color='green')
	tup = []
	for i in range(0,len(y)):
		# print(y[i])
		tup.append(int(y[i]))
	for i, v in enumerate(tup):
		plt.text(v + 2, i -0.25, str(v), color='blue', fontsize=6)
	plt.show()
	

# Call this functions in order to see graphs
#comparisonBAV()
# strongestSUV()
# countCars()
# oldestCars()
# mostExpensive(1000,20000)
# compareSpecs()
# strongestCars()	
mycursor.close()

