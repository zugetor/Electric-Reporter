from flask import Blueprint, jsonify, session, request, redirect, url_for, render_template
import node

app = Blueprint('NODE', __name__)

@app.route('/register')
def register():	
	try:
		id = request.args.get("id")
		if(id is None):
			return jsonify({"status":False,"error":"id should not be null"}), 400
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
		if(id is None):
			return jsonify({"status":False,"error":"id should not be null"}), 400
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
		if(id is None and message is None):
			return jsonify({"status":False,"error":"id and message should not be null"}), 400
		if(id is None):
			return jsonify({"status":False,"error":"id should not be null"}), 400
		if(message is None):
			return jsonify({"status":False,"error":"message should not be null"}), 400
		if node.room_report(id,message):
			return jsonify({"status":True})
		else:
			return jsonify({"status":False})
	except Exception as e:
		return jsonify({"error": str(e),"status":False}), 500

@app.route('/logs')
def log():	
	try:
		id = request.args.get("id")
		if(id is None):
			return jsonify({"status":False,"error":"id should not be null"}), 400
		res = jsonify(node.getlog(id))
		if res:
			return res
		else:
			return jsonify({"status":False})
	except Exception as e:
		return jsonify({"error": str(e),"status":False}), 500

@app.route('/delete-report')
def del_report():	
	try:
		id = request.args.get("id")
		message = request.args.get("message")
		if(id is None and message is None):
			return jsonify({"status":False,"error":"id and message should not be null"}), 400
		if(id is None and id != ""):
			return jsonify({"status":False,"error":"id should not be null"}), 400
		if(message is None):
			return jsonify({"status":False,"error":"message should not be null"}), 400
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
		if(id is None and volt is None and amp is None and watt is None):
			return jsonify({"status":False,"error":"id, volt, amp and watt should not be null"}), 400
		if(id is None):
			return jsonify({"status":False,"error":"id should not be null"}), 400
		if(volt is None):
			return jsonify({"status":False,"error":"volt should not be null"}), 400
		if(amp is None):
			return jsonify({"status":False,"error":"amp should not be null"}), 400
		if(watt is None):
			return jsonify({"status":False,"error":"watt should not be null"}), 400
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
		if(id is None and schedule is None):
			return jsonify({"status":False,"error":"id and schedule should not be null"}), 400
		if(id is None):
			return jsonify({"status":False,"error":"id should not be null"}), 400
		if(schedule is None):
			return jsonify({"status":False,"error":"schedule should not be null"}), 400
		if schedule:
			schedule['status'] = True
			return jsonify(schedule)
		else:
			return jsonify({"status":False}), 500
	except Exception as e:
		return jsonify({"error": str(e)}), 500