# Polovni Automobili Webscraper

Using __BeautifulSoup__ python library to extract information about cars on website www.polovniautomobili.com from car ads
and inserting them into mysql database.

Did not extract all data from car ads, only essential like mileage, power, type, engine volume etc.

With this data we can analyze various information, for example which car model of a certain brand has the best corelation betweeen price, age, engine volume, etc. Other than that, we can have statistical information about car performances in general and difference between prices. 


In other file, **analysis.py**, there are functions that manages to extract certain type of data needed to analyze various parameters that already exists in given database. The goal is to visualize through graphs and charts, and explain usage of data in some database. There are several problems that was looked into that can be modified.




