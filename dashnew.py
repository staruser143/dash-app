from flask import Flask, request, jsonify, make_response
import jwt
import datetime
from functools import wraps
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# App configurations
SECRET_KEY = "your_secret_key"
REFRESH_SECRET_KEY = "your_refresh_secret_key"
app = Flask(__name__)

# Utility: Generate Tokens
def generate_tokens(user_id, roles):
    # Access Token (short-lived)
    access_payload = {
        "sub": user_id,
        "roles": roles,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    }
    access_token = jwt.encode(access_payload, SECRET_KEY, algorithm="HS256")

    # Refresh Token (long-lived)
    refresh_payload = {
        "sub": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }
    refresh_token = jwt.encode(refresh_payload, REFRESH_SECRET_KEY, algorithm="HS256")

    return access_token, refresh_token

# Mock Authentication (Replace with Directory API integration)
def authenticate_user(credentials):
    if credentials["username"] == "admin" and credentials["password"] == "admin123":
        return {"id": "1", "roles": ["admin"]}
    elif credentials["username"] == "user" and credentials["password"] == "user123":
        return {"id": "2", "roles": ["user"]}
    return None

# Middleware: Validate Access Token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get("auth_token")
        if not token:
            return jsonify({"message": "Unauthorized"}), 401
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.user = payload
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Access token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401
        return f(*args, **kwargs)
    return decorated

# Login Endpoint
@app.route('/login', methods=['POST'])
def login():
    credentials = request.json
    user = authenticate_user(credentials)
    if user:
        access_token, refresh_token = generate_tokens(user["id"], user["roles"])
        response = make_response(jsonify({"message": "Login successful"}))
        response.set_cookie("auth_token", access_token, httponly=True, secure=True)
        response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True)
        return response
    return jsonify({"message": "Invalid credentials"}), 401

# Refresh Endpoint
@app.route('/refresh', methods=['POST'])
def refresh():
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        return jsonify({"message": "Missing refresh token"}), 401
    try:
        payload = jwt.decode(refresh_token, REFRESH_SECRET_KEY, algorithms=["HS256"])
        user_id = payload["sub"]
        access_token, new_refresh_token = generate_tokens(user_id, ["user"])  # Example roles
        response = make_response(jsonify({"message": "Token refreshed"}))
        response.set_cookie("auth_token", access_token, httponly=True, secure=True)
        response.set_cookie("refresh_token", new_refresh_token, httponly=True, secure=True)
        return response
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Refresh token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid refresh token"}), 401