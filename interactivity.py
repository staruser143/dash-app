import dash
from dash import dcc, html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id='my-dropdown',
        options=[
            {'label': 'Option 1', 'value': 'OPT1'},
            {'label': 'Option 2', 'value': 'OPT2'}
        ],
        value='OPT1'
    ),
    dcc.Graph(id='my-graph')
])

@app.callback(
    Output('my-graph', 'figure'),
    Input('my-dropdown', 'value')
)
def update_graph(selected_value):
    # Here you can define how the graph updates based on the selected_value.
    # For example, you might want to filter your data based on the selected_value.
    # In this example, we'll just change the title of the graph.
    return {
        'data': [{'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'}],
        'layout': {'title': f'Selected value: {selected_value}'}
    }

if __name__ == '__main__':
    app.run_server(debug=True)
    