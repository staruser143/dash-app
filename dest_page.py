import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash

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
    # Parse the URL to get the user_id parameter
    query = dash.utils.parse_query_string(search)
    user_id = query.get('user_id', 'No user_id')
    return f'User ID: {user_id}'

if __name__ == '__main__':
    app.run_server(debug=True)