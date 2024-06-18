import dash
from dash import dcc, html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id='my-dropdown',
        options=[
            {'label': 'Option 1', 'value': 'OPT1'},
            {'label': 'Option 2', 'value': 'OPT2'},
            {'label': 'Option 3', 'value': 'OPT3'}
        ],
        multi=True
    ),
    html.Div(id='dropdown-output-container')
])

@app.callback(
    Output('dropdown-output-container', 'children'),
    Input('my-dropdown', 'value')
)
def update_output(selected_values):
    if selected_values:
        return f'You have selected: {", ".join(selected_values)}'
    else:
        return 'No option selected'
    
if __name__ == '__main__':
    app.run_server(debug=True)