from dash import dcc, html

layout = html.Div([
    html.H1('Page 2'),
    dcc.Link('Go back to home', href='/'),
])