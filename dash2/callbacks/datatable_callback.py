from dash import Output, Input
from sqlalchemy import create_engine, text
import logging
import pandas as pd
#from ..\dbutils import parse_filter_query
# import parse_filter_query from dbutils
from callbacks.dbutils import parse_filter_query
logger = logging.getLogger(__name__)
# Create an engine that uses a connection pool
engine = create_engine('sqlite:///my_database.db', pool_size=10, max_overflow=20)


def register_datatable_callback(app):
    
    @app.callback(
        Output('table', 'data'),
        Output('table', 'columns'),
        Output('table', 'page_count'),
        Output('table', 'style_data_conditional'),
        Input('table', 'page_current'),
        Input('table', 'page_size'),
        Input('table', 'filter_query'),
        Input('table', 'sort_by'))  
    def update_table(page_current, page_size, filter_query,sort_by):
        logging.info(f"START: update_table")
        logger.info(f"page_current: {page_current}")
        logger.info(f"page_size: {page_size}")
        logger.info(f"filter_query: {filter_query}")
        logger.info(f"sort_by: {sort_by}")
    
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

        where_clause = ''
        if filter_query:
            where_clause =" where " + parse_filter_query(filter_query) 
        

        logger.info(f"where_clause: {where_clause}")

        # Execute a SQL query to fetch the data for the current page
        query = text(f"SELECT * FROM employees {where_clause} {order_by} LIMIT :start, :count").bindparams(start=start_idx, count=page_size)
        # Compile the query with literal binds
        compiled_query = str(query.compile(engine, compile_kwargs={"literal_binds": True}))
        logger.info(f'Debug Query is: {compiled_query}')

        df = pd.read_sql_query(query, engine, params={"start": start_idx, "count": page_size})
        
        style_data_conditional = [
            {
                'if': {'column_id': col},
            'textAlign': 'left' if df[col].dtype == 'O' else 'right'
            }
            for col in df.columns
        ] +     [
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'  # color for odd rows
            },
            {
                'if': {'row_index': 'even'},
                'backgroundColor': 'white'  # color for even rows
            }
        ]
        
        # Execute a SQL query to count the total number of records
        if filter_query:
            count_query = text("SELECT COUNT(*) FROM employees  " + where_clause)
        else:
            count_query = text("SELECT COUNT(*) FROM employees")

        connection = engine.connect()
        total_count = connection.execute(count_query).scalar()
        connection.close()

        # Calculate the total number of pages
        page_count = -(-total_count // page_size)  # Equivalent to math.ceil(total_count / page_size)
        
        logger.info(f"END: update_table")
        # Return the data, columns, and page_count for the DataTable
        return df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], page_count, style_data_conditional

    