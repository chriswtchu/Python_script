#import moledule
import sys
import os
import re
import math
import csv
import sqlite3

#input parameter
#input parameter - check the parameterfile name
parameterfile = raw_input("parameterfile: ")

try:
	open(parameterfile , "r")
except IOError, ioex:
	print "Parameter file does not exist. Please check."

#Appetizer
#Appetizer - read parameterfile
def getvarfromfile(filename):
	import imp
	with open(filename , "r") as importfile:
		global data
		data = imp.load_source("data", "", importfile)

getvarfromfile(parameterfile)

#Appetizer - remove existing data base
try:
	os.remove(data.databasename + ".db")
except OSError:
	pass

#Appetizer - create database
database = sqlite3.connect(data.databasename + ".db")
cursor =  database.cursor()

#Main course1 - input data
cursor.execute("""CREATE TABLE dbtable (date text, trans text, symbol text, qty real, price real)""")
cursor.execute("""INSERT INTO dbtable VALUES ('2006-01-05','BUY','RHAT',100,35.14)""")
database.commit()

#Main course2 - execute query
t = ('RHAT',)
cursor.execute('SELECT * FROM dbtable WHERE symbol=?', t)

print "---------------------------------------"
print cursor.fetchone()
print "---------------------------------------"

purchases = [('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
             ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
             ('2006-04-06', 'SELL', 'IBM', 500, 53.00),
            ]
cursor.executemany('INSERT INTO dbtable VALUES (?,?,?,?,?)', purchases)

cursor.execute('SELECT * FROM dbtable')

with open("sample.csv" , "wb") as csv_file:
	csv_writer = csv.writer(csv_file)
	csv_writer.writerow([i[0] for i in cursor.description])
	csv_writer.writerows(cursor)


#Tea - close opened file
database.close()

