import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import pandas as pd
import psycopg2
# Callback to update table structure based on selected table
def register_callbacks(app):
    @app.callback(
         [Output('table-structure', 'data'),
         Output('table-structure', 'columns'),
         Output('table-data', 'data'),
         Output('table-data', 'columns')],
         [Input('table-dropdown', 'value')]
    )
    def update_table_structure(selected_table):
        if selected_table is not None:
            query ="""
                    SELECT distinct c.column_name, c.data_type, c.is_nullable, c.column_default, c.ordinal_position, col_description(pg_class.oid, c.ordinal_position) AS column_comment, obj_description(pg_class.oid, 'pg_class') AS table_comment
                    FROM information_schema.columns c
                    JOIN pg_class ON c.table_name = pg_class.relname
                    LEFT JOIN pg_description ON pg_class.oid = pg_description.objoid
                    WHERE c.table_name = %s AND c.table_schema = 'public'
                    ORDER BY c.ordinal_position
                    """
            conn=psycopg2.connect(
                dbname='mydatabase',
                user='postgres',
                password='mysecretpassword',
                host='localhost',
                port='5432')
            cursor=conn.cursor()
            cursor.execute(query, (selected_table,))
            columns = cursor.fetchall()
            
            # Assuming you want to display column name, data type, and comments
            df = pd.DataFrame(columns, columns=['Name', 'Type', 'Not Null', 'Default Value', 'Position', 'Column Comment', 'Table Comment'])
            
            # Since the table comment is the same for all rows, you might want to handle it differently
            # For simplicity, it's included in every row here
            
            structure_data = df.to_dict('records')
            print(f"Structure data: {structure_data}")
            structure_columns = [{"name": i, "id": i} for i in df.columns]

            # New logic to fetch table data
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {selected_table};")
            data_rows = cursor.fetchall()
            data_columns = [desc[0] for desc in cursor.description]
            data_df = pd.DataFrame(data_rows, columns=data_columns)

            data_data = data_df.to_dict('records')
            data_columns = [{"name": i, "id": i} for i in data_df.columns]

            return structure_data, structure_columns, data_data, data_columns
        else:
            return [], [], [], []
    return "Select a table to view its structure."