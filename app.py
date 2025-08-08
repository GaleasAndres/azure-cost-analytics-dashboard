from flask import Flask, session, send_from_directory, render_template_string
from config import FLASK_SECRET_KEY
from backend.auth.azure_auth import auth_bp
from backend.api import api_bp
import os

app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY

app.register_blueprint(auth_bp)
app.register_blueprint(api_bp, url_prefix="/api")

# Simple login page template
LOGIN_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Azure Cost Analytics - Login</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #333;
        }
        
        .login-container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 3rem;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
            text-align: center;
            max-width: 400px;
            width: 90%;
        }
        
        .logo {
            font-size: 3rem;
            color: #667eea;
            margin-bottom: 1rem;
        }
        
        h1 {
            font-size: 1.8rem;
            font-weight: 600;
            color: #2d3748;
            margin-bottom: 0.5rem;
        }
        
        p {
            color: #718096;
            margin-bottom: 2rem;
            line-height: 1.6;
        }
        
        .login-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 1rem 2rem;
            border-radius: 12px;
            font-size: 1.1rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        }
        
        .login-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 35px rgba(102, 126, 234, 0.6);
        }
        
        .features {
            margin-top: 2rem;
            text-align: left;
        }
        
        .features h3 {
            color: #2d3748;
            margin-bottom: 1rem;
            font-size: 1.1rem;
        }
        
        .feature-list {
            list-style: none;
            color: #718096;
        }
        
        .feature-list li {
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .feature-list i {
            color: #667eea;
            font-size: 0.9rem;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="logo">
            <i class="fas fa-chart-line"></i>
        </div>
        <h1>Azure Cost Analytics</h1>
        <p>Sign in to access your Azure cost analytics dashboard and monitor your cloud spending.</p>
        
        <a href="/auth/login" class="login-btn">
            <i class="fas fa-sign-in-alt"></i>
            Sign in with Azure
        </a>
        
        <div class="features">
            <h3>What you'll get:</h3>
            <ul class="feature-list">
                <li><i class="fas fa-chart-bar"></i> Real-time cost analytics</li>
                <li><i class="fas fa-layer-group"></i> Resource group breakdowns</li>
                <li><i class="fas fa-chart-area"></i> Daily cost trends</li>
                <li><i class="fas fa-shield-alt"></i> Secure Azure AD authentication</li>
            </ul>
        </div>
    </div>
</body>
</html>
"""

# Serve frontend/index.html at "/" for authenticated users, login page for others
@app.route("/")
def home():
    # Check if user is authenticated
    if "user" in session and "access_token" in session:
        # User is authenticated, serve the dashboard
        return send_from_directory(os.path.join(app.root_path, "frontend"), "index.html")
    else:
        # User is not authenticated, serve the login page
        return render_template_string(LOGIN_PAGE)

# Serve frontend assets (app.js, styles.css) at their URLs
@app.route("/<path:filename>")
def frontend_files(filename):
    return send_from_directory(os.path.join(app.root_path, "frontend"), filename)

if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5000)
