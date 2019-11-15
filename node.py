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

def updateConfig(id,campus,building,room):
	con = sqlite3.connect(DATABASE)
	completion = False
	with con:
		cur = con.cursor()
		cur.execute("UPDATE config SET campus = ? , building = ? , room = ? WHERE nodeId = ?",(campus,building,room,id))
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
			cur.execute("INSERT INTO log VALUES(?,?,?,?)",(id,volt,amp,watt))
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