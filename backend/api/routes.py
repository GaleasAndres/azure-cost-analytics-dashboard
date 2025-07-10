# backend/api/routes.py

from flask import Blueprint, jsonify

api_bp = Blueprint("api_bp", __name__)

@api_bp.route("/hello")
def hello():
    return jsonify({"message": "Hello from /api/hello!"})