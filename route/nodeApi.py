from flask import Blueprint, jsonify, session, request, redirect, url_for, render_template
import requests,json
import urllib.parse
import node, user
import datetime, time, pytz

app = Blueprint('NODE', __name__)
tz = pytz.timezone('Asia/Bangkok')

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
		thisNode = node.getNode(id)
		if node.room_report(id,message):
			admin = user.getAdmin()
			for i in admin:
				line_text("\nRoom: "+thisNode[4]+"\nMessage: "+message,i[3])
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
		raw = node.getSchedule(id)	
		if(id is None and raw is None):
			return jsonify({"status":False,"error":"id and room should not be null"}), 400
		if(id is None):
			return jsonify({"status":False,"error":"id should not be null"}), 400
		if(raw is None):
			return jsonify({"status":False,"error":"room should not be null"}), 400		
		if raw:
			day = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
			day = day[datetime.datetime.now(tz).weekday()]
			hour = datetime.datetime.now(tz).hour
			if(day in raw.keys()):
				schedule = raw[day]
				index = -1
				for i, item in enumerate(schedule):
					if(item["start_time"] >= hour and hour <= item["end_time"]):
						index = i
						break
				time_table = []
				if(index > -1):				
					time_table.append(schedule[i])
					if(index < len(schedule)-2):
						time_table.append(schedule[i+1])
				else:
					res = jsonify({"status":False})
					return res
				res = jsonify({"status":True,"data":time_table})
				return res
			else:
				return jsonify({"status":False}), 400
		else:
			return jsonify({"status":False}), 500
	except Exception as e:
		return jsonify({"error": str(e)}), 500
		
def line_text(message,token):	
	try:
		msg = urllib.parse.urlencode({"message":message})
		LINE_HEADERS = {'Content-Type':'application/x-www-form-urlencoded',"Authorization":"Bearer "+token}
		session = requests.Session()
		a=session.post("https://notify-api.line.me/api/notify" , headers=LINE_HEADERS, data=msg)
	except Exception as e:
		print(e)