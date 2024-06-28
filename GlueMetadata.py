import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_table
import boto3
import pandas as pd

# Function to fetch table names from AWS Glue Catalog
def fetch_glue_tables(database_name):
    glue_client = boto3.client('glue')
    response = glue_client.get_tables(DatabaseName=database_name)
    table_list = [table['Name'] for table in response['TableList']]
    return table_list

# Function to fetch details of a selected table
def fetch_table_details(database_name, table_name):
    glue_client = boto3.client('glue')
    response = glue_client.get_table(DatabaseName=database_name, Name=table_name)
    table_details = response['Table']
    # Convert table details to a format suitable for displaying in a DataTable
    details_df = pd.DataFrame([table_details])
    return details_df

# Initialize Dash app
app = dash.Dash(__name__)

# Set the layout for the app
app.layout = html.Div([
    html.H1("AWS Glue Catalog Table Details"),
    dcc.Dropdown(id='table-dropdown', options=[], value=None),
    dash_table.DataTable(id='table-details')
])

@app.callback(
    Output('table-dropdown', 'options'),
    Input('table-dropdown', 'value')  # Dummy input for initialization
)
def update_dropdown(_):
    database_name = "your_database_name_here"  # Set your database name
    table_names = fetch_glue_tables(database_name)
    # Create options for the Dropdown
    options = [{'label': name, 'value': name} for name in table_names]
    return options

@app.callback(
    Output('table-details', 'columns'),
    Output('table-details', 'data'),
    Input('table-dropdown', 'value')
)
def update_table_details(selected_table):
    if selected_table is None:
        return [], []
    database_name = "your_database_name_here"  # Set your database name
    details_df = fetch_table_details(database_name, selected_table)
    # Prepare columns and data for the DataTable
    columns = [{"name": i, "id": i} for i in details_df.columns]
    data = details_df.to_dict('records')
    return columns, data

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)