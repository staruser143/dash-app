import dash_core_components as dcc
import dash_html_components as html

layout = html.Div([
    dcc.Link('Go to Page 2 with user_id=123', href='/page-2?user_id=123')
])