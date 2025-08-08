from flask import Blueprint, redirect, url_for, session, request, jsonify
import msal
import uuid
import time
from config import CLIENT_ID, CLIENT_SECRET, AUTHORITY, REDIRECT_PATH, SCOPE

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/auth")

def _build_msal_app(cache=None):
    return msal.ConfidentialClientApplication(
        CLIENT_ID, authority=AUTHORITY,
        client_credential=CLIENT_SECRET, token_cache=cache)

def _build_auth_url(state=None):
    return _build_msal_app().get_authorization_request_url(
        SCOPE,
        state=state or str(uuid.uuid4()),
        redirect_uri=url_for("auth_bp.callback", _external=True)
    )

@auth_bp.route("/login")
def login():
    session["state"] = str(uuid.uuid4())
    auth_url = _build_auth_url(session["state"])
    return redirect(auth_url)

@auth_bp.route("/callback")
def callback():
    if request.args.get('state') != session.get("state"):
        return "State mismatch!", 400
    if "error" in request.args:
        return f"Error: {request.args['error']}", 400

    code = request.args.get("code")
    result = _build_msal_app().acquire_token_by_authorization_code(
        code,
        scopes=SCOPE,
        redirect_uri=url_for("auth_bp.callback", _external=True)
    )
    if "access_token" in result:
        session["user"] = result.get("id_token_claims")
        session["access_token"] = result["access_token"]
        if "expires_in" in result:
            session["token_expires"] = int(time.time()) + int(result["expires_in"])
        # Redirect to the main dashboard after successful login
        return redirect(url_for('home'))
    else:
        return jsonify({"error": result.get("error"), "desc": result.get("error_description")})

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(
        f"{AUTHORITY}/oauth2/v2.0/logout"
        f"?post_logout_redirect_uri={url_for('read_root', _external=True)}"
    )
