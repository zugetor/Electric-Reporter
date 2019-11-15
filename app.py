from flask import Flask, g, render_template, session, redirect, url_for, escape, request, jsonify
import sqlite3, os
import user
from route import auth, admin

DATABASE = "./database.db"

# Create app
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'super-secret'
app.register_blueprint(auth.app)
app.register_blueprint(admin.app, url_prefix="/admin")

# check if the database exist, if not create the table and insert a few lines of data
if not os.path.exists(DATABASE):
	conn = sqlite3.connect(DATABASE)
	cur = conn.cursor()
	cur.execute("CREATE TABLE users (username TEXT, password TEXT, permission INTEGER);")
	cur.execute("CREATE TABLE log (nodeId TEXT, volt FLOAT, amp FLOAT, watt FLOAT);")
	cur.execute("CREATE TABLE config (nodeId TEXT, building TEXT, room TEXT);")
	conn.commit()
	user.register("admin","admin",1)
	user.register("user","user")

# helper method to get the database since calls are per thread,
# and everything function is a new thread when called
def get_db():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = sqlite3.connect(DATABASE)
	return db


# helper to close
@app.teardown_appcontext
def close_connection(exception):
	db = getattr(g, '_database', None)
	if db is not None:
		db.close()

@app.route("/")
def index():
	if 'username' in session:
		sess_user = user.getUser(session["username"])
		if(not sess_user or (sess_user and sess_user[2] != session['permission'])):
			session.pop('username', None)
			session.pop('permission', None)
			return redirect(url_for('AUTH.login'))
		return render_template("index.html", sess=session)
	return redirect(url_for('AUTH.login'))

@app.route("/settings")
def settings():
	if 'username' in session and session['permission'] == 1:
		sess_user = user.getUser(session["username"])
		if(not sess_user or (sess_user and sess_user[2] != session['permission'])):
			session.pop('username', None)
			session.pop('permission', None)
			return redirect(url_for('AUTH.login'))
		cur = get_db().cursor()
		res = cur.execute("select * from users")
		return render_template("settings.html", sess=session, users=res)
	return redirect(url_for('index'))


if __name__ == "__main__":
	print(app.url_map)
	app.run()