import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Input(
        id='my-input',
        type='text',
        value='initial value'
    ),
    html.Button('Submit', id='my-button'),
    html.Div(id='my-output')
])
@app.callback(
    Output('my-output', 'children'),
    Input('my-button', 'n_clicks'),
    State('my-input', 'value')
)
def update_output(n_clicks, input_value):
    if n_clicks is None:
        # Button has not been clicked yet
        return ''
    else:
        return f'You have entered: {input_value}'

if __name__ == '__main__':
    app.run_server(debug=True)