from flask import Blueprint, jsonify, request
from buu import Room

api = Blueprint('RoomAPI', __name__)
room = Room()

@api.route("/")
def index():
	try:
		campusid = request.args.get('campus')
		bc = request.args.get('building')
		if(campusid is None and bc is None):
			return jsonify({"error":"campus and building should not be null"}), 400
		if(campusid is None):
			return jsonify({"error":"campus should not be null"}), 400
		if(bc is None):
			return jsonify({"error":"building should not be null"}), 400
		res = jsonify(room.getAll(campusid,bc))
		res.cache_control.max_age = 604800
		res.headers.add('Access-Control-Allow-Origin', '*')
		return res
	except Exception as e:
		return jsonify({"error": str(e)}), 500

@api.route("/schedule")
def schedule():
	try:
		campusid = request.args.get('campus')
		roomid = request.args.get('room')
		if(campusid is None and roomid is None):
			return jsonify({"error":"campus and room should not be null"}), 400
		if(campusid is None):
			return jsonify({"error":"campus should not be null"}), 400
		if(roomid is None):
			return jsonify({"error":"room should not be null"}), 400
		res = jsonify(room.getSchedule(campusid, roomid))
		res.cache_control.max_age = 3600
		res.headers.add('Access-Control-Allow-Origin', '*')
		return res
	except Exception as e:
		return jsonify({"error": str(e)}), 500
