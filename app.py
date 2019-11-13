from flask import Flask, g, render_template, session, redirect, url_for, escape, request, jsonify
import sqlite3
import os
import user

DATABASE = "./database.db"

# Create app
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'super-secret'

# check if the database exist, if not create the table and insert a few lines of data
if not os.path.exists(DATABASE):
	conn = sqlite3.connect(DATABASE)
	cur = conn.cursor()
	cur.execute("CREATE TABLE users (username TEXT, password TEXT, permission INTEGER);")
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
		cur = get_db().cursor()
		res = cur.execute("select * from users")
		return render_template("index.html", users=res, curUser=session['username'],permission=session['permission'])
	return redirect(url_for('login'))
	
	
@app.route('/login', methods=['GET', 'POST'])
def login():
	if 'username' in session:
		return redirect(url_for('index'))
	
	if request.method == 'POST':
		username = request.form['username']
		pwd = request.form['password']		
		if(user.validate(username,pwd)):
			session['username'] = username
			session['permission'] = user.getUser(username)[2]
			return redirect(url_for('index'))
		else:
			return redirect(url_for('login'))
	
	return '''
		<form method="post">
			<p><input type=text name=username>
			<p><input type=text name=password>
			<p><input type=submit value=Login>
		</form>
	'''

@app.route('/logout')
def logout():
	# remove the username from the session if it's there
	session.pop('username', None)
	return redirect(url_for('index'))


if __name__ == "__main__":
	"""
	Use python sqlite3 to create a local database, insert some basic data and then
	display the data using the flask templating.
	
	http://flask.pocoo.org/docs/0.12/patterns/sqlite3/
	"""
	app.run()