import sqlite3
from sqlite3 import Error
import pandas as pd
import encode_image as e



#gets the connection to a databse and returns that connection
def create_server_connection(db_file):
	connection = None
	try:
		connection = sqlite3.connect(db_file)
		#print("got emm")
	except Error as err:
		print("Data base unable to be created")

	return connection


#sets up the data base that stores all of the sensor information stores the following info
#	elementIndex integer PRIMARY KEY,  //one of a kind element, search by this or second
#	second integer, 				   //reasonable to search by as more then likely time does not flow backwards
#	temp text,						   //the rest are stored as text as the numbers are floting point not integers
#	humidity text,
#	pressure text,
#
#	gpsLAT text,
#	gpsLONG text,
#
#	gyroX text,
#	gyroY text,
#	gyroZ text,
#
#	accelX text,
#	accelY text,
#	accelZ text,
#
#	img BLOB							//picture being stored
#use ether pullInd to get a specific elemnt or pullTime to get an elemnt at a certian time
def setUp_DB(db_connection):
	sensorTable = """CREATE TABLE IF NOT EXISTS sensor(
	elementIndex integer PRIMARY KEY,
	second integer,
	temp text,
	humidity text,
	pressure text,

	gpsLAT text,
	gpsLONG text,

	gyroX text,
	gyroY text,
	gyroZ text,

	accelX text,
	accelY text,
	accelZ text,

	img BLOB
	); """

	#machineTable = """CREATE TABLE IF NOT EXISTS machineLearning(); """

	#faultTable = """CREATE TABLE IF NOT EXISTS faultManagement(); """

	try:
		c = db_connection.cursor()
		c.execute(sensorTable)
		db_connection.commit()
	except Error as e:
		print(e + "unable to add sensorTable")

	#print(sensorTable)
#gets the ino in args as a tuple and creates a new element in the sensor database
#tuple in order of:
#(elementIndex, second, tempature, humidity, pressure,  gpsLAT,gpsLONG,  gyroX,gyroY,gyroZ,   accelX,accelY,accelZ, imgname)
def sensorPush(db_connection, args):
	sensorSQL = """INSERT INTO sensor(elementIndex, second, temp, humidity, pressure,gpsLAT,gpsLONG,gyroX,gyroY,gyroZ, accelX,accelY,accelZ, img)
	VALUES(?,?,?,?,?, ?,? ,?,?,?, ?,?,?, ?)"""
	c = db_connection.cursor()
	c.execute(sensorSQL, args)
	db_connection.commit()

#deletes an element at the index of index,
#warning that inforamtion is gone, use it to clean database
def deleteSensor(db_connection, index):
	sensorSQL = """ DELETE FROM sensor WHERE elementIndex = ?"""
	c = db_connection.cursor()
	c.execute(sensorSQL,index)
	db_connection.commit()

#gets all rows that currently exist in the sensor relation and returns it, return is an array of an array of strings
#each returned subarray will have 14 elements in the order it was stored
#the image is just the image name that refrences where ever image was stored
def pullall(db_connection):
	pullSQL = """SELECT * FROM sensor"""
	c = db_connection.cursor()
	c.execute(pullSQL)

	rows = c.fetchall()
	return rows
	#for row in rows:
		#print(row)
	#db_connection.commit()

#gets the row with the index, index in sensor and returns it
#the returned array will have 14 elements in the order it was stored
#the image is just the image name that refrences where ever image was stored
def pullInd(db_connection,index):
	pullSQL = """SELECT * From sensor where elementIndex = ?"""
	c = db_connection.cursor()
	c.execute(pullSQL, str(index))

	rows = c.fetchall()
	return rows

#gets the row(s) with a certian time in sensor and returns it, return is an array
#the returned array will have 14 elements in the order it was stored
#the image is just the image name that refrences where ever image was stored
def pullTime(db_connection, second):
	pullSQL = """SELECT * From sensor where second = ?"""
	c = db_connection.cursor()
	c.execute(pullSQL, str(second))

	rows = c.fetchall()

	return rows
	#for row in rows:
	#	print(row)

#gets the number of elements in the sensor database
def pullCount(db_connection):
	pullSQL = """SELECT COUNT(*) From sensor """
	c = db_connection.cursor()
	c.execute(pullSQL)

	rows = c.fetchall()

	return rows[0][0]

#test area
def main():
	con = create_server_connection("flight.db")
	global senPusnum
	senPusnum = 0
	if con is None:
		return
	setUp_DB(con)

	print(pullCount(con))
	#for x in range(5):
	#	sensordata = (senPusnum,1,"test","test","test", "test","test", "test","test","test", "test","test","test", "nameless.jpg")
	#	senPusnum +=1
	#	sensorPush(con,sensordata)


	#pullall(con)

	#for i in range(senPusnum):
	#	deleteSensor(con, str(i))
	#print(con)



main()