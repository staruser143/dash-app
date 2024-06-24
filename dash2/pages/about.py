from dash import html,dcc

layout=html.Div([
    html.H1('Hello Dash'),
    html.Div(' Select US States.'),
    html.Div(id="demo1"),
    # Add a dropdown with values from 1 to 25
    dcc.Dropdown(
        id='input1-dropdown',
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        value='NYC'  # Default value
    ),

])
