from flask import Blueprint, jsonify, session, request, redirect, url_for, render_template
import user, node

app = Blueprint('ADMIN', __name__)

@app.route('/register', methods=['GET', 'POST'])
def register():	
	try:
		if request.method == 'POST' and 'username' in session and session['permission'] == 1:
			sess_user = user.getUser(session["username"])
			if(not sess_user or (sess_user and sess_user[2] != session['permission'])):
				session.pop('username', None)
				session.pop('permission', None)
				return redirect(url_for('AUTH.login'))		
			if("username" not in request.form or "password" not in request.form):
				return redirect(url_for('settings'))
			username = request.form['username']
			pwd = request.form['password']			
			permission = 0
			user.register(username, pwd, permission)
			return redirect(url_for('settings'))
		else:
			return redirect(url_for('index'))
	except Exception:
		return redirect(url_for('index'))

@app.route('/config')
def config():
	try:
		if 'username' in session and session['permission'] == 1:
			sess_user = user.getUser(session["username"])
			if(not sess_user or (sess_user and sess_user[2] != session['permission'])):
				session.pop('username', None)
				session.pop('permission', None)
				return redirect(url_for('AUTH.login'))
			id = request.args.get("id")
			campus = request.args.get("campus")
			building = request.args.get("building")
			room = request.args.get("room")
			roomName = request.args.get("name")
			if(id is None or campus is None or building is None or room is None or roomName is None):
				return redirect(url_for('settings'))
			node.updateConfig(id, campus, building, room, roomName)
			return redirect(url_for('settings'))
		else:
			return redirect(url_for('index'))
	except Exception:
		return redirect(url_for('index'))
			
@app.route('/permission')
def permission():
	try:
		if 'username' in session and session['permission'] == 1:
			sess_user = user.getUser(session["username"])
			if(not sess_user or (sess_user and sess_user[2] != session['permission'])):
				session.pop('username', None)
				session.pop('permission', None)
				return redirect(url_for('AUTH.login'))
			username = request.args.get("username")
			permission = request.args.get("permission")
			if(username is None or permission is None):
				return redirect(url_for('settings'))
			user.setUserPermission(username, permission)
			return redirect(url_for('settings'))
		else:
			return redirect(url_for('index'))
	except Exception:
		return redirect(url_for('index'))
		
@app.route('/token')
def token():
	try:
		if 'username' in session and session['permission'] == 1:
			sess_user = user.getUser(session["username"])
			if(not sess_user or (sess_user and sess_user[2] != session['permission'])):
				session.pop('username', None)
				session.pop('permission', None)
				return redirect(url_for('AUTH.login'))
			username = request.args.get("username")
			token = request.args.get("token")
			if(username is None or token is None):
				return redirect(url_for('settings'))
			user.setLineToken(username, token)
			return redirect(url_for('settings'))
		else:
			return redirect(url_for('index'))
	except Exception:
		return redirect(url_for('index'))
		
@app.route('/delete')
def delete():
	try:
		if 'username' in session and session['permission'] == 1:
			sess_user = user.getUser(session["username"])
			if(not sess_user or (sess_user and sess_user[2] != session['permission'])):
				session.pop('username', None)
				session.pop('permission', None)
				return redirect(url_for('AUTH.login'))
			username = request.args.get("username")
			if(username is None):
				return redirect(url_for('settings'))
			user.delUser(username)
			return redirect(url_for('settings'))
		else:
			return redirect(url_for('index'))
	except Exception:
		return redirect(url_for('index'))