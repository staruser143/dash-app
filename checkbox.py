import dash
from dash import dcc, html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Checklist(
        id='my-checkbox',
        options=[
            {'label': 'Option 1', 'value': 'OPT1'},
            {'label': 'Option 2', 'value': 'OPT2'}
        ],
        value=['OPT1']
    ),
    html.Div(id='checkbox-output-container')
])
@app.callback(
    Output('checkbox-output-container', 'children'),
    Input('my-checkbox', 'value')
)
def update_output(selected_values):
    return f'You have selected: {", ".join(selected_values)}'

if __name__ == '__main__':
    app.run_server(debug=True)
    