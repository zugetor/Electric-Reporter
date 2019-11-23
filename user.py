import sqlite3, hashlib, base64

DATABASE = "./database.db"

def register(username, password, permission=0):
	con = sqlite3.connect(DATABASE)
	completion = False
	token = None
	with con:
		cur = con.cursor()
		if(getUser(username) is None):
			cur = con.cursor()
			cur.execute("INSERT INTO users (username, password, permission,token) VALUES (?,?,?,'')",(username,encrypt(password),permission))
			con.commit()
			completion = True
	return completion
	
def validate(username, password):
	con = sqlite3.connect(DATABASE)
	completion = False
	with con:
		cur = con.cursor()
		cur.execute("select * from users WHERE username = ?",(username,))
		row = cur.fetchone()
		if(row is None):
			return False
		dbUser = row[0]
		dbPass = row[1]
		if dbUser == username:
			completion = _check_password(dbPass, password)
	return completion
	
def getUser(username):
	con = sqlite3.connect(DATABASE)
	with con:
		cur = con.cursor()
		cur.execute("select * from users WHERE username = ?",(username,))
		return cur.fetchone()
		
def getAdmin():
	con = sqlite3.connect(DATABASE)
	with con:
		cur = con.cursor()
		cur.execute("select * from users WHERE permission = ?",(1,))
		return cur.fetchall()

def setUserPermission(username, permission):
	con = sqlite3.connect(DATABASE)
	completion = False
	with con:
		cur = con.cursor()
		cur.execute("UPDATE users SET permission = ? WHERE username = ?",(permission,username))
		con.commit()
		completion = True
	return completion	
	
def setLineToken(username,token):
	con = sqlite3.connect(DATABASE)
	completion = False
	with con:
		cur = con.cursor()
		cur.execute("UPDATE users SET token = ? WHERE username = ?",(token,username))
		con.commit()
		completion = True
	return completion	


def delUser(username):
	con = sqlite3.connect(DATABASE)
	completion = False
	with con:
		cur = con.cursor()
		cur.execute("DELETE from users WHERE username = ?",(username,))
		con.commit()
		completion = True	
	return completion
	
def _check_password(hashed_password, user_password):
	return hashed_password == encrypt(user_password)
	
def encrypt(data):
	return base64.b64encode(hashlib.sha512(data.encode()).digest())