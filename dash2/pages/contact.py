from dash import html,dcc

layout=html.Div([
    html.H1('Hello Dash'),
    html.Div('Select Indian States.'),
    html.Div(id="demo2"),
    # Add a dropdown with values from 1 to 25
    dcc.Dropdown(
        id='input2-dropdown',
        options=[
            {'label': 'Chennai', 'value': 'CHN'},
            {'label': 'Bengalure', 'value': 'BLR'}
        ],
        value='CHN'  # Default value
    ),

])
