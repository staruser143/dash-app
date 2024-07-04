import dash
from dash import html, dcc, Input, Output, State

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Input(id='username', type='text', placeholder='Username'),
    dcc.Input(id='password', type='password', placeholder='Password'),
    html.Button('Login', id='login-button'),
    html.Div(id='login-output'),
    dcc.Interval(id='token-renewal-interval', interval=1000*60*5, n_intervals=0)  # every 5 minutes
])

@app.callback(
    Output('login-output', 'children'),
    Input('login-button', 'n_clicks'),
    State('username', 'value'),
    State('password', 'value')
)
def login(n_clicks, username, password):
    if n_clicks:
        auth_response = authenticate_user(username, password)
        if auth_response:
            user_details = fetch_user_details(auth_response['user_id'])
            return f"Welcome, {user_details['name']}"
        else:
            return "Authentication failed"
    return ""

@app.callback(
    Output('token-renewal-interval', 'n_intervals'),
    Input('token-renewal-interval', 'n_intervals')
)
def renew_access_token(n_intervals):
    renew_token()
    return n_intervals

if __name__ == '__main__':
    app.run_server(debug=True)
