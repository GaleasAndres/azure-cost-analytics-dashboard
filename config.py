import os
from dotenv import load_dotenv

# Load .env file at startup
load_dotenv()

CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
TENANT_ID = os.getenv("AZURE_TENANT_ID")
CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("AZURE_REDIRECT_URI")
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
REDIRECT_PATH = "/auth/callback"  # Must match your Azure App Registration

# OAuth scopes: "User.Read" lets you test login; for Azure Resource APIs, use Azure scopes
SCOPE = [
    "https://management.azure.com/.default",
    "https://management.core.windows.net/.default"
]

SESSION_TYPE = "filesystem"  # Optional, but recommended for Flask session
