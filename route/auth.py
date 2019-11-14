from flask import Blueprint, jsonify, session, request, redirect, url_for, render_template
import user

app = Blueprint('AUTH', __name__)

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
			return render_template("login.html",user=username)
	
	return render_template("login.html",user="")

@app.route('/logout')
def logout():
	# remove the username from the session if it's there
	session.pop('username', None)
	session.pop('permission', None)
	return redirect(url_for('index'))