import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from urllib.parse import parse_qs

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='user-id-display')
])

@app.callback(
    Output('user-id-display', 'children'),
    [Input('url', 'search')]
)
def display_user_id(search):
    # Parse the query string
    parsed_search = parse_qs(search.lstrip('?'))
    # Extract the user_id parameter
    user_id = parsed_search.get('user_id', ['No user_id'])[0]  # Get the first value
    return f'User ID: {user_id}'

if __name__ == '__main__':
    app.run_server(debug=True)