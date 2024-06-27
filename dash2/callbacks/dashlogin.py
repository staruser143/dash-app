import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc

# Initialize the Dash app with a Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout of the app
app.layout = dbc.Container([
    dbc.Row(
        dbc.Col(
            dbc.Form([
                dbc.Row([
                    dbc.Label("Username", className="mr-2", width=10),
                    dbc.Col(dbc.Input(type="text", id="username-input", placeholder="Enter username"), width=10),
                ], className="mb-3"),
                dbc.Row([
                    dbc.Label("Password", className="mr-2", width=10),
                    dbc.Col(dbc.Input(type="password", id="password-input", placeholder="Enter password"), width=10),
                ], className="mb-3"),
                dbc.Button("Login", color="primary", id="login-button"),
            ], style={'width': '300px'}),
            width=6
        ),
        justify="center",
        align="center",
        style={"height": "100vh"},
    ),
])

# Callback for the login button
@app.callback(
    Output('login-button', 'children'),  # Just as an example, changing button text
    [Input('login-button', 'n_clicks')],
    [State('username-input', 'value'), State('password-input', 'value')]
)
def update_output(n_clicks, username, password):
    if n_clicks is not None:
        # Here, you would add your authentication logic
        if username == 'admin' and password == 'secret':
            return 'Success'
        else:
            return 'Failed'
    return 'Login'

if __name__ == '__main__':
    app.run_server(debug=True)