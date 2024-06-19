import pandas as pd
import dash
from dash import html, dash_table, Input, Output, callback


from dash.exceptions import PreventUpdate
from sqlalchemy_filters import apply_filters
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from pyparsing import Word, alphas, alphanums,  quotedString, removeQuotes, delimitedList, Group

import employeeModel
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
        sort_by=[] , # Initialize sort_by to an empty list
        filter_action='custom',  # Enable filtering
        filter_query=''  # Initialize filter_query to an empty string
    )
])


# Define the basic elements of the filter query syntax
column_name = Word(alphas, alphanums + '_').setParseAction(removeQuotes)
value = quotedString.setParseAction(removeQuotes)
operator = Word("eq ne lt le gt ge", exact=1)

# Define the syntax for a condition
condition = Group(column_name + operator + value)

# Define the syntax for a filter query
filter_query_parser = delimitedList(condition, delim='&&')

def filter_query_to_sqlalchemy(filter_query):
    if not filter_query:
        raise PreventUpdate

    # Use the filter_query parser to parse a filter query string
    parsed_filter_query = filter_query_parser.parseString(filter_query)

    # Convert the parsed filter query to a list of conditions
    conditions = [{'field': cond[0], 'op': cond[1], 'value': cond[2]} for cond in parsed_filter_query]

    return conditions




# Add filter_query as an input
@app.callback(
    Output('table', 'data'),
    Output('table', 'columns'),
    Output('table', 'page_count'),
    Input('table', 'page_current'),
    Input('table', 'page_size'),
    Input('table', 'sort_by'),
    Input('table', 'filter_query'))  
def update_table(page_current, page_size, sort_by, filter_query):
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

    # Parse the filter_query into a list of conditions
    conditions = filter_query_to_sqlalchemy(filter_query)

    # Create a SQLAlchemy session
    engine = create_engine('sqlite:///your_database.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    # Create a SQLAlchemy query
    query = session.query(employeeModel)

    # Apply the filters to the query
    filtered_query = apply_filters(query, conditions)

    # Execute the filtered query to fetch the data for the current page
    df = pd.read_sql_query(filtered_query.statement.compile(engine, compile_kwargs={"literal_binds": True}), engine)

    # Execute a SQL query to count the total number of records
    count_query = text(f"SELECT COUNT(*) FROM employees")
    connection = engine.connect()
    total_count = connection.execute(count_query).scalar()
    connection.close()

    # Calculate the total number of pages
    page_count = -(-total_count // page_size)  # Equivalent to math.ceil(total_count / page_size)

    # Return the data, columns, and page_count for the DataTable
    return df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], page_count


if __name__ == '__main__':
    app.run_server(debug=True)