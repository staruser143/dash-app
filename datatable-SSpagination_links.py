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
        page_size=10,
        page_count=1  # Initialize page_count to 1
    )
])

@app.callback(
    Output('table', 'data'),
    Output('table', 'columns'),
    Output('table', 'page_count'),  # Add an output for page_count
    Input('table', 'page_current'),
    Input('table', 'page_size'))
def update_table(page_current, page_size):
    # Calculate the indices of the data for the current page
    start_idx = page_current * page_size
    end_idx = (page_current + 1) * page_size

    # Execute a SQL query to fetch the data for the current page
    query = text("SELECT * FROM employees LIMIT :start, :end")
    df = pd.read_sql_query(query, engine, params={"start": start_idx, "end": page_size})

    # Execute a SQL query to count the total number of records
    count_query = text("SELECT COUNT(*) FROM employees")
    # Get a connection from the engine
    connection = engine.connect()
    total_count = connection.execute(count_query).scalar()

    # Calculate the total number of pages
    page_count = -(-total_count // page_size)  # Equivalent to math.ceil(total_count / page_size)

    # Return the data, columns, and page_count for the DataTable
    return df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], page_count

if __name__ == '__main__':
    app.run_server(debug=True)