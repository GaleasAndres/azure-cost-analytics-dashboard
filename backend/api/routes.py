from flask import jsonify, Response

from . import api_bp


@api_bp.route('/hello')
def hello_world() -> Response:
    """Return a greeting from the API blueprint."""
    return jsonify(message='Hello from API')
