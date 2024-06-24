from dash import html,dcc

layout2=html.Div([
    html.H1('Hello Dash'),
    html.Div('Dash: A web application framework for Python.'),
    html.Div(id="demo2"),
    # Add a dropdown with values from 1 to 25
    dcc.Dropdown(
        id='input2-dropdown',
        options=[
            {'label': 'Chennai', 'value': 'CHN'},
            {'label': 'Bengaluru', 'value': 'BLR'}
        ],
        value='CHN'  # Default value
    ),

])
