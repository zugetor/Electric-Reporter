from flask import Blueprint, jsonify
from buu import Building

api = Blueprint('BuildingAPI', __name__)
building = Building()

@api.route("/")
def index():
	try:
		res = jsonify(building.getAll())
		res.cache_control.max_age = 604800
		res.headers.add('Access-Control-Allow-Origin', '*')
		return res
	except Exception as e:
		return jsonify({"error": str(e)}), 500