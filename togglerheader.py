import dash
from dash import html, dcc, Input, Output
import dash_table
import pandas as pd

# Sample DataFrame to populate the DataTable, can be empty initially
df = pd.DataFrame({
    "Column 1": [],
    "Column 2": [],
    # Add more columns as needed
})

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H3('Table Header', id='table-header', style={'display': 'none'}),  # Initially hidden
    dash_table.DataTable(
        id='datatable',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
    ),
])

@app.callback(
    Output('table-header', 'style'),
    [Input('datatable', 'data')]
)
def toggle_header_visibility(rows):
    if rows:  # If there are rows in the data
        return {'display': 'block'}  # Show header
    else:
        return {'display': 'none'}  # Hide header

if __name__ == '__main__':
    app.run_server(debug=True)