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
		return jsonify({"error": str(e),"status":False}), 500

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