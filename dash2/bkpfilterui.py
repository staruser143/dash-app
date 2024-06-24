
import dash
from dash import html,dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

app=dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = dbc.Container([
    # Add a H2 Header
    dbc.Row([
        dbc.Col(html.H2('Filter UI Example')),
    ], className='mb-3'),
    dbc.Row([
        dbc.Col(html.Label('Select Field', htmlFor='field-dropdown'), width=2),
        dbc.Col(dcc.Dropdown(
            id='field-dropdown',
            options=[
                {'label': 'Field 1', 'value': 'field1'},
                {'label': 'Field 2', 'value': 'field2'},
                # Add more fields as needed
            ],
            placeholder='Select a field'
        ), width=10),
    ], className='mb-3'),  # mb-3 adds margin-bottom for spacing between rows

    # Add more rows for additional inputs
    # Example for another dropdown (e.g., operator dropdown)
    dbc.Row([
        dbc.Col(html.Label('Select Operator', htmlFor='operator-dropdown'), width=2),
        dbc.Col(dcc.Dropdown(
            id='operator-dropdown',
            options=[
                {'label': '>', 'value': '>'},
                {'label': '<', 'value': '<'},
                # Add more operators as needed
            ],
            placeholder='Select an operator'
        ), width=10),
    ], className='mb-3'),
    # Add a Input Field
    dbc.Row([
        dbc.Col(html.Label('Enter Value', htmlFor='value-input'), width=2),
        dbc.Col(dcc.Input(
            id='value-input',
            type='text',
            placeholder='Enter filter value'
        ), width=10),
    ], className='mb-3'),
    # Add more components as needed
    # Add a Submit button
    dbc.Row([
        dbc.Col(dbc.Button('Submit', color='primary', id='submit-button'), width=2),
    ]),
], fluid=True)


#Start the dash app
if __name__ == '__main__':
    app.run_server(debug=True)