from flask import Blueprint, jsonify, session, request, redirect, url_for, render_template
import node

app = Blueprint('NODE', __name__)

@app.route('/register')
def register():	
	try:
		id = request.args.get("id")
		if id != "" and id is not None and node.register(id):
			return jsonify({"status":True})
		else:
			return jsonify({"status":False})
	except Exception as e:
		return jsonify({"error": str(e),"status":False}), 

@app.route('/delete')
def delete():	
	try:
		id = request.args.get("id")
		if id != "" and id is not None and node.delete(id):
			return redirect(url_for('settings'))
		else:
			return redirect(url_for('settings'))
	except Exception as e:
		return redirect(url_for('settings'))

@app.route('/room-report')
def room_report():	
	try:
		id = request.args.get("id")
		message = request.args.get("message")
		if node.room_report(id,message):
			return jsonify({"status":True})
		else:
			return jsonify({"status":False})
	except Exception as e:
		return jsonify({"error": str(e),"status":False}), 500

@app.route('/delete-report')
def del_report():	
	try:
		id = request.args.get("id")
		message = request.args.get("message")
		if node.deleteRoom_report(id,message):
			return redirect(url_for('settings'))
		else:
			return redirect(url_for('settings'))
	except Exception as e:
		return redirect(url_for('settings'))

@app.route('/report')
def report():	
	try:
		id = request.args.get("id")
		volt = request.args.get("volt")
		amp = request.args.get("amp")
		watt = request.args.get("watt")
		if node.report(id,volt,amp,watt):
			return jsonify({"status":True})
		else:
			return jsonify({"status":False})
	except Exception as e:
		return jsonify({"error": str(e),"status":False}), 500

@app.route('/schedule')
def schedule():
	try:
		id = request.args.get("id")
		schedule = node.getSchedule(id)
		if schedule:
			schedule['status'] = True
			return jsonify(schedule)
		else:
			return jsonify({"status":False}), 500
	except Exception as e:
		return jsonify({"error": str(e)}), 500