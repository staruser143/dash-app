

from dash import dcc, html, dash_table
import psycopg2

def fetch_table_names():
    conn=psycopg2.connect(
    dbname='mydatabase',
    user='postgres',
    password='mysecretpassword',
    host='localhost',
    port='5432')
    cursor = conn.cursor()
    # Query to select table names from the current schema
    # You might want to filter by schema if you have multiple schemas
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
    """)
    tables = cursor.fetchall()
    return [table[0] for table in tables]

layout = html.Div([
    dcc.Dropdown(
        id='table-dropdown',
        options=[{'label': table, 'value': table} for table in fetch_table_names()],
        placeholder="Select a table"
    ),
    dash_table.DataTable(id='table-structure'),
    dash_table.DataTable(id='table-data')  # This is the new DataTable for displaying the selected table's data
])

def create_table_layout():
    return layout