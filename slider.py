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
    dcc.Slider(
        id='my-slider',
        min=0,
        max=20,
        step=0.5,
        value=10,
    ),
    html.Div(id='slider-output-container')
])

@app.callback(
    Output('slider-output-container', 'children'),
    Input('my-slider', 'value')
)
def update_output(value):
    return f'You have selected "{value}"'

if __name__ == '__main__':
    app.run_server(debug=True)
    