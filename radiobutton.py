import dash
from dash import dcc, html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.RadioItems(
        id='my-radio',
        options=[
            {'label': 'Option 1', 'value': 'OPT1'},
            {'label': 'Option 2', 'value': 'OPT2'}
        ],
        value='OPT1'
    ),
    html.Div(id='radio-output-container')
])

@app.callback(
    Output('radio-output-container', 'children'),
    Input('my-radio', 'value')
)
def update_output(selected_value):
    return f'You have selected: {selected_value}'

if __name__ == '__main__':
    app.run_server(debug=True)

    