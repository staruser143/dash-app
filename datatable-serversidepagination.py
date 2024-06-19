import pandas as pd
import dash
from dash import html, dash_table, Input, Output
from sqlalchemy import create_engine, text

# Create an engine that uses a connection pool
engine = create_engine('sqlite:///my_database.db', pool_size=10, max_overflow=20)

# Create a Dash app
app = dash.Dash(__name__)

# Initialize the DataTable with empty data
app.layout = html.Div([
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in pd.DataFrame().columns],
        data=[],
        page_action='custom',
        page_current=0,
        page_size=1,
    )
])

@app.callback(
    Output('table', 'data'),
    Output('table', 'columns'),
    Input('table', 'page_current'),
    Input('table', 'page_size'))
def update_table(page_current, page_size):
    # Calculate the indices of the data for the current page
    start_idx = page_current * page_size
    end_idx = (page_current + 1) * page_size

    # Execute a SQL query to fetch the data for the current page
    query = text("SELECT * FROM employees LIMIT :start, :end")
    df = pd.read_sql_query(query, engine, params={"start": start_idx, "end": end_idx})

    # Return the data and columns for the DataTable
    return df.to_dict('records'), [{"name": i, "id": i} for i in df.columns]

if __name__ == '__main__':
    app.run_server(debug=True)