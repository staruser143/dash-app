import dash
from dash import dcc, html  
from dash.dependencies import Input, Output
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(id='my-dynamic-dropdown'),
    html.Button('Submit', id='submit-button', n_clicks=0)
])



@app.callback(
    Output('my-dynamic-dropdown', 'options'),
    Input('submit-button', 'n_clicks')
)
def update_dropdown_options(n_clicks):
    # Replace this with your own logic to generate options
    options = [{'label': f'Option {i}', 'value': f'OPT{i}'} for i in range(n_clicks)]
    return options

if __name__ == '__main__':
    app.run_server(debug=True)