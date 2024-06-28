import dash
from dash import html,dcc
from dash.dependencies import Input, Output, State
import psycopg2
from flask import session
from flask_session import Session
from flask import Flask
server=Flask(__name__)
server.config['SESSION_TYPE'] = 'filesystem'
Session(server)

# Initialize Dash app
app = dash.Dash(__name__,server=server)
app.server.secret_key = 'your_secret_key'

# Configure server-side session
#app.config['SESSION_TYPE'] = 'filesystem'
#Session(app)

# Define layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

login_layout = html.Div([
    dcc.Input(id='username', type='text', placeholder='Username'),
    dcc.Input(id='password', type='password', placeholder='Password'),
    html.Button('Login', id='login-button'),
    html.Div(id='login-output')
])
app.layout=login_layout
# Callback for login
@app.callback(Output('login-output', 'children'),
              [Input('login-button', 'n_clicks')],
              [State('username', 'value'), State('password', 'value')])
def login(n_clicks, username, password):
    if n_clicks is None:
        return ''
    conn = psycopg2.connect('dbname=my_database, user=postgres, password=mysecretpassword ,host=localhost, port=5432')
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cur.fetchone()
    cur.close()
    conn.close()
    if user:
        session['auth_user'] = username
        return 'Login Successful!'
    else:
        return 'Invalid Credentials'

# Callback to control page access
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def page_control(pathname):
    if pathname == '/login':
        return login_layout
    elif 'auth_user' not in session:
        return login_layout
    else:
        return html.Div('Welcome to the protected page!')

if __name__ == '__main__':
    app.run_server(debug=True)