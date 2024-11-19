from flask import Flask, request, make_response, g
from dash import Dash, html, Input, Output, dcc
import requests
import jwt
import dash_bootstrap_components as dbc
import datetime

# Flask App
server = Flask(__name__)
server.secret_key = "your-secret-key"

# Public key for token verification (obtained from Auth server)
PUBLIC_KEY = "your-public-key"

# Simulate Auth Server (replace with your actual auth server call)
def authenticate_user(username, password):
    # Mock authentication (replace with actual API request)
    if username == "admin" and password == "password123":
        token_payload = {
            "username": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        return jwt.encode(token_payload, "your-secret-key", algorithm="HS256")
    raise Exception("Invalid credentials")

# Middleware: Verify token for all requests except `/login`
@server.before_request
def verify_token():
    if request.path == "/login":
        return
    token = request.cookies.get('access_token')
    if not token:
        return "Unauthorized: No token provided", 401
    try:
        decoded_token = jwt.decode(token, "your-secret-key", algorithms=["HS256"])
        g.user = decoded_token["username"]  # Save user in Flask global
    except jwt.ExpiredSignatureError:
        return "Unauthorized: Token has expired", 401
    except jwt.InvalidTokenError:
        return "Unauthorized: Invalid token", 401

# Login endpoint
@server.route('/login', methods=['POST'])
def login():
    data = request.json  # Expecting JSON with username and password
    username = data.get('username')
    password = data.get('password')
    try:
        token = authenticate_user(username, password)
        response = make_response({"message": "Login successful"})
        response.set_cookie(
            'access_token', token, httponly=True, secure=True, samesite="Strict"
        )
        return response
    except Exception as e:
        return {"message": str(e)}, 401

# Logout endpoint
@server.route('/logout', methods=['POST'])
def logout():
    response = make_response({"message": "Logged out"})
    response.set_cookie('access_token', '', expires=0)  # Clear token
    return response

# Dash App
app = Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.H1("Stateless Session with Dash"),
    dcc.Location(id="url"),
    html.Div(id="content"),
])

# Authenticated page layout
def get_dashboard_layout(username):
    return html.Div([
        html.H3(f"Welcome, {username}!"),
        html.Button("Logout", id="logout-btn", n_clicks=0),
    ])

# Login page layout
login_layout = html.Div([
    html.H3("Login"),
    dbc.Input(id="username", placeholder="Username", type="text"),
    dbc.Input(id="password", placeholder="Password", type="password", className="mt-2"),
    dbc.Button("Login", id="login-btn", color="primary", className="mt-2"),
    html.Div(id="login-message", className="mt-2"),
])

@app.callback(
    Output("content", "children"),
    Input("url", "pathname")
)
def render_page(pathname):
    if pathname == "/" and hasattr(g, "user"):
        return get_dashboard_layout(g.user)
    return login_layout

@app.callback(
    Output("login-message", "children"),
    Input("login-btn", "n_clicks"),
    [Input("username", "value"), Input("password", "value")]
)
def login_user(n_clicks, username, password):
    if n_clicks > 0:
        try:
            response = requests.post(
                "http://localhost:5000/login", 
                json={"username": username, "password": password}
            )
            if response.status_code == 200:
                return "Login successful! Refresh the page."
            return response.json().get("message", "Login failed")
        except Exception as e:
            return str(e)
    return ""

@app.callback(
    Output("url", "pathname"),
    Input("logout-btn", "n_clicks")
)
def logout_user(n_clicks):
    if n_clicks > 0:
        requests.post("http://localhost:5000/logout")  # Call logout endpoint
        return "/"
    return "/"

# Run Server
if __name__ == "__main__":
    app.run_server(debug=True)