from sqlalchemy_filters import apply_filters
from sqlalchemy import text, create_engine
from sqlalchemy.orm import sessionmaker
from dash.exceptions import PreventUpdate
import employeeModel

from dash.exceptions import PreventUpdate
from sqlalchemy_filters import apply_filters
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from pyparsing import Word, alphas, alphanums,  quotedString, removeQuotes, delimitedList, Group 
# Define the basic elements of the filter query syntax
column_name = Word(alphas, alphanums + '_').setParseAction(removeQuotes)
value = quotedString.setParseAction(removeQuotes)
operator = Word("eq ne lt le gt ge", exact=1)

# Define the syntax for a condition
condition = Group(column_name + operator + value)

# Define the syntax for a filter query
filter_query_parser = delimitedList(condition, delim='&&')

from pyparsing import Word, alphas, alphanums,  quotedString, removeQuotes, delimitedList, Group 

# Define the basic elements of the filter query syntax
column_name = Word(alphas, alphanums + '_').setParseAction(removeQuotes)
value = quotedString.setParseAction(removeQuotes)
operator = Word("eq ne lt le gt ge", exact=1)

# Define the syntax for a condition
condition = Group(column_name + operator + value)

# Define the syntax for a filter query
filter_query_parser = delimitedList(condition, delim='&&')

def filter_query_to_sqlalchemy(filter_query):
    print("START: filter_query_to_sqlalchemy")
    print("filter_query: ", filter_query)

    if not filter_query:
        raise PreventUpdate

    # Use the filter_query parser to parse a filter query string
    parsed_filter_query = filter_query_parser.parseString(filter_query)
    print("parsed_filter_query: ", parsed_filter_query)
    # Convert the parsed filter query to a list of conditions
    conditions = [{'field': cond[0], 'op': cond[1], 'value': cond[2]} for cond in parsed_filter_query]
    print("conditions: ", conditions)
    print("END: filter_query_to_sqlalchemy")

    return conditions

def filter_query_to_sql(filter_query):
    if not filter_query:
        raise PreventUpdate

    # Parse the filter_query into a list of conditions
    conditions = []
    for condition_str in filter_query.split(' && '):
        column_name, operator, value = condition_str.split(' ')
        column_name = column_name.strip('{}')
        value = value.strip("'")
        conditions.append({'field': column_name, 'op': operator, 'value': value})

    # Create a SQLAlchemy session
    engine = create_engine('sqlite:///your_database.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    # Create a SQLAlchemy query
    query = session.query(employeeModel)

    # Apply the filters to the query
    filtered_query = apply_filters(query, conditions)

    # Convert the filtered query to SQL
    filtered_sql = str(filtered_query.statement.compile(engine, compile_kwargs={"literal_binds": True}))

    # Close the session
    session.close()

    return filtered_sql