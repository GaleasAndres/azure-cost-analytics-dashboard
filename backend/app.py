"""Flask application entrypoint."""

from flask import Flask, jsonify, Response


def create_app() -> Flask:
    """Create and configure the Flask application."""

    app = Flask(__name__)

    @app.route("/")
    def read_root() -> Response:
        """Return a friendly greeting."""
        return jsonify(message="Hello, World!")

    from api import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

