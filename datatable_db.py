import pandas as pd
import dash
from dash import html,dash_table

# Establish a connection to the SQLite database
#connection = sqlite3.connect('your_database.db')

from sqlalchemy import create_engine,text

# Create an engine that uses a connection pool
engine = create_engine('sqlite:///my_database.db', pool_size=10, max_overflow=20)

# Get a connection from the pool
connection = engine.connect()


# Execute a SQL query to fetch the data from the table
query = "SELECT * FROM employees"
df = pd.read_sql_query(query, connection)

# Close the connection
connection.close()

# Create a Dash app
app = dash.Dash(__name__)

# Use the DataFrame to populate the Dash DataTable
app.layout = html.Div([
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)