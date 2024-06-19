import pandas as pd
import dash
from dash import html, dash_table, Input, Output
from sqlalchemy import create_engine, text

# Create an engine that uses a connection pool
engine = create_engine('sqlite:///my_database.db', pool_size=10, max_overflow=20)

# Create a Dash app
app = dash.Dash(__name__)

# Initialize the DataTable with empty data and enable sorting
app.layout = html.Div([
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in pd.DataFrame().columns],
        data=[],
        page_action='custom',
        page_current=0,
        page_size=10,
        page_count=1,  # Initialize page_count to 1
        sort_action='custom',  # Enable sorting
        #sort_mode='multi',  # Allow sorting by multiple columns
        sort_by=[]  # Initialize sort_by to an empty list
    )
])

@app.callback(
    Output('table', 'data'),
    Output('table', 'columns'),
    Output('table', 'page_count'),
    Input('table', 'page_current'),
    Input('table', 'page_size'),
    Input('table', 'sort_by'))  # Add sort_by as an input
def update_table(page_current, page_size, sort_by):
    # Calculate the indices of the data for the current page
    start_idx = page_current * page_size

    # Build the ORDER BY clause for the SQL query
    if len(sort_by):
        order_by = 'ORDER BY ' + ', '.join(
            f"{col['column_id']} {'ASC' if col['direction'] == 'asc' else 'DESC'}"
            for col in sort_by
        )
    else:
        order_by = ''

    # Execute a SQL query to fetch the data for the current page
    query = text(f"SELECT * FROM employees {order_by} LIMIT :start, :count")
    print(f'Query is:{query}')
    df = pd.read_sql_query(query, engine, params={"start": start_idx, "count": page_size})

    # Execute a SQL query to count the total number of records
    count_query = text("SELECT COUNT(*) FROM employees")
    connection = engine.connect()
    total_count = connection.execute(count_query).scalar()
    connection.close()

    # Calculate the total number of pages
    page_count = -(-total_count // page_size)  # Equivalent to math.ceil(total_count / page_size)

    # Return the data, columns, and page_count for the DataTable
    return df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], page_count


if __name__ == '__main__':
    app.run_server(debug=True)