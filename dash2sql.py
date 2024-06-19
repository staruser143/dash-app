from dash import Dash, dash_table, html, Input, Output, State
import pandas as pd
import sqlite3
import json

from sqlalchemy import create_engine, text

from util_dash2sql import dash_filter_to_sql

app = Dash(__name__)
# Create an engine that uses a connection pool
engine = create_engine('sqlite:///my_database.db', pool_size=10, max_overflow=20)

app.layout = html.Div([
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in pd.DataFrame().columns],
        filter_action='custom',
        filter_query=''
    ),
    html.Div(id='output')
])

@app.callback(
    Output('table', 'data'),
    Input('table', 'filter_query')
)
def update_table(filter_query):
    print(f"Start: update_table")
    if not filter_query:
        query = "SELECT * FROM employees"
    else:
        print(f"filter_query: {filter_query}")
        filters = json.loads(filter_query)
        where_clause = dash_filter_to_sql(filters)
        print(f"where_clause: {where_clause}")
        query = f"SELECT * FROM employees WHERE {where_clause}"
        print(f"query: {query}")
        df = pd.read_sql_query(query, engine)
        return df.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)