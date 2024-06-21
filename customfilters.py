import pandas as pd
import dash
from dash import html, dcc, dash_table, Input, Output


# Create a Dash app
app = dash.Dash(__name__)


app.layout = html.Div([
    dcc.Dropdown(
        id='field-dropdown',
        options=[{'label': i, 'value': i} for i in  pd.DataFrame().columns]
       
    ),
    dcc.Dropdown(
        id='operator-dropdown',
        options=[{'label': i, 'value': i} for i in ['=', '!=', '>', '<', '>=', '<=']]
    ),
    dcc.Input(
        id='value-input',
        type='text'
    ),
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in  pd.DataFrame().columns],
        data=df.to_dict('records')
    )
])

@app.callback(
    Output('table', 'data'),
    [Input('field-dropdown', 'value'),
     Input('operator-dropdown', 'value'),
     Input('value-input', 'value')]
)
def update_table(field, operator, value):
    if field is not None and operator is not None and value is not None:
        dff = df.query(f'{field} {operator} {value}')
        return dff.to_dict('records')
    return dash.no_update