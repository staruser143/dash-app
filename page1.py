from dash import dcc, html

layout = html.Div([
    html.H1('Page 1 how r u'),
    dcc.Link('Go back to home', href='/'),
])