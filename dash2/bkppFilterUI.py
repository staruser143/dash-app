import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State

# Initialize the Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    
    # Create a Label for dropdown field
    html.Label('Select Field',htmlFor='field-dropdown'),
    dcc.Dropdown(
        id='field-dropdown',
        options=[
            {'label': 'Field 1', 'value': 'field1'},
            {'label': 'Field 2', 'value': 'field2'},
            # Add more fields as needed
        ],
        placeholder='Select a field'
    ),
    # Create a Label for operator dropdown
    html.Label('Select Operator',htmlFor='operator-dropdown'),
    dcc.Dropdown(
        id='operator-dropdown',
        options=[
            {'label': '>', 'value': '>'},
            {'label': '<', 'value': '<'},
            {'label': 'Contains', 'value': 'contains'},
            {'label': 'Starts With', 'value': 'startsWith'},
            # Add more operators as needed
        ],
        placeholder='Select an operator'
    ),
    # Create a Label for value input
    html.Label('Enter Value',htmlFor='value-input'),
    dcc.Input(
        id='value-input',
        type='text',
        placeholder='Enter filter value'
    ),
    html.Button('Submit', id='submit-button', n_clicks=0),
    html.Div(id='output-container')
])


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)