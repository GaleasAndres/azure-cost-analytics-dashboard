from flask import jsonify

from . import api_bp


@api_bp.route('/hello')
def hello_world():
    return jsonify(message='Hello from API')
