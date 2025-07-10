from flask import Flask, jsonify
app = Flask(__name__)


@app.route("/")
def read_root():
    return jsonify(message="Hello, World!")


from api import api_bp

app.register_blueprint(api_bp, url_prefix="/api")


if __name__ == "__main__":
    app.run(debug=True)

