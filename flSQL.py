import sqlite3
from sqlite3 import Error
import pandas as pd

def create_server_connection(db_file):
	connection = None
	try:
		connection = sqlite3.connect(db_file)
		print("got emm")
	except Error as err:
		print("no good")

	return connection

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

	machineTable = """CREATE TABLE IF NOT EXISTS machineLearning(); """

	faultTable = """CREATE TABLE IF NOT EXISTS faultManagement(); """

	try:
		c = db_connection.cursor()
		c.execute(sensorTable)
		db_connection.commit()
	except Error as e:
		print(e + "unable to add sensorTable")

	#print(sensorTable)

def sensorPush(db_connection, args):
	sensorSQL = """INSERT INTO sensor(elementIndex, second, temp, humidity, pressure,gpsLAT,gpsLONG,gyroX,gyroY,gyroZ, accelX,accelY,accelZ, img)
	VALUES(?,?,?,?,?, ?,? ,?,?,?, ?,?,?, ?)"""
	c = db_connection.cursor()
	c.execute(sensorSQL, args)
	db_connection.commit()

def deleteSensor(db_connection, index):
	sensorSQL = """ DELETE FROM sensor WHERE elementIndex = ?"""
	c = db_connection.cursor()
	c.execute(sensorSQL,index)
	c.commit()

def sensorPull(db_connection, index):
	print("q")

def main():
	con = create_server_connection("flight.db")
	senPusnum = 1
	if con is None:
		return
	setUp_DB(con)
	sensordata = (senPusnum,1,"test","test","test", "test","test", "test","test","test", "test","test","test", "nameless.jpg:")
	senPusnum +=1
	sensorPush(con,sensordata)
	for i in range(senPusnum):
		deleteSensor(con, i)
	#print(con)

main()