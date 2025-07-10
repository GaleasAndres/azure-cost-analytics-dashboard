from flask import Flask, session, send_from_directory
from config import FLASK_SECRET_KEY
from backend.auth.azure_auth import auth_bp
from backend.api import api_bp
import os

app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY

app.register_blueprint(auth_bp)
app.register_blueprint(api_bp, url_prefix="/api")

# Serve frontend/index.html at "/"
@app.route("/")
def home():
    return send_from_directory(os.path.join(app.root_path, "frontend"), "index.html")

# Serve frontend assets (app.js, styles.css) at their URLs
@app.route("/<path:filename>")
def frontend_files(filename):
    return send_from_directory(os.path.join(app.root_path, "frontend"), filename)

if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5000)
