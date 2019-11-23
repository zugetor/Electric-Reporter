from time import time
import sqlite3
from buu import Room

DATABASE = "./database.db"
room = Room()

def register(id):
	con = sqlite3.connect(DATABASE)
	completion = False
	with con:
		cur = con.cursor()
		if(getNode(id) is None):
			cur = con.cursor()
			cur.execute("INSERT INTO config (nodeId) VALUES(?)",(id,))
			con.commit()
			completion = True
	return completion

def updateConfig(id,campus,building,room, name):
	con = sqlite3.connect(DATABASE)
	completion = False
	with con:
		cur = con.cursor()
		cur.execute("UPDATE config SET campus = ? , building = ? , room = ? , name = ? WHERE nodeId = ?",(campus,building,room,name,id))
		con.commit()
		completion = True
	return completion

def delete(id):
	con = sqlite3.connect(DATABASE)
	completion = False
	with con:
		cur = con.cursor()
		cur.execute("DELETE from config WHERE nodeId = ?",(id,))
		con.commit()
		cur.execute("DELETE from log WHERE nodeId = ?",(id,))
		con.commit()
		completion = True
	return completion	

def getAllNode():
	con = sqlite3.connect(DATABASE)
	with con:
		cur = con.cursor()
		cur.execute("select * from config")
		return cur.fetchall()

def getNode(id):
	con = sqlite3.connect(DATABASE)
	with con:
		cur = con.cursor()
		cur.execute("select * from config WHERE nodeId = ?",(id,))
		return cur.fetchone()

def report(id,volt,amp,watt):
	con = sqlite3.connect(DATABASE)
	completion = False
	with con:
		cur = con.cursor()
		if(getNode(id) is not None):
			cur = con.cursor()
			cur.execute("INSERT INTO log VALUES(?,?,?,?,?)",(id,volt,amp,watt,int(time())))
			con.commit()
			completion = True
	return completion

def room_report(id,message):
	con = sqlite3.connect(DATABASE)
	completion = False
	with con:
		cur = con.cursor()
		node = getNode(id)
		if(node is not None):
			cur = con.cursor()
			cur.execute("INSERT INTO report VALUES(?,?,?,?)",(id,node[4],message,int(time())))
			con.commit()
			completion = True
	return completion

def getRoom_report():
	con = sqlite3.connect(DATABASE)
	with con:
		cur = con.cursor()
		cur.execute("select * from report")
		return cur.fetchall()

def deleteRoom_report(id,subject):
	con = sqlite3.connect(DATABASE)
	completion = False
	with con:
		cur = con.cursor()
		cur.execute("DELETE from report WHERE nodeId = ? AND message = ?",(id,subject))
		con.commit()
		completion = True
	return completion	

def getSchedule(id):
	completion = False
	config = getNode(id)
	if(config is not None):
		campus = {"Bangsaen": 1,"Juntaburi": 2,"Srakaew": 3}
		res = room.getSchedule(campus[config[1]], config[3])
		return res
	return completion

def getlog(id):
	con = sqlite3.connect(DATABASE)
	with con:
		cur = con.cursor()
		cur.execute("SELECT * from log WHERE nodeId = ?",(id,))
		return cur.fetchall()