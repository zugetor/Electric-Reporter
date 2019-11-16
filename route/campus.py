from flask import Blueprint, jsonify
from buu import Campus

api = Blueprint('CampusAPI', __name__)

@api.route("/")
def index():
	res = jsonify(Campus.getAll())
	res.cache_control.max_age = 604800
	res.headers.add('Access-Control-Allow-Origin', '*')
	return res