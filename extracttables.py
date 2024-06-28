import sqlparse
from sqlparse.sql import IdentifierList, Identifier
from sqlparse.tokens import Name, Whitespace, Wildcard

def extract_tables(sql):
    # Parse the SQL query
    parsed = sqlparse.parse(sql)
    tables = set()

    for item in parsed:
        # Recursively traverse the parsed tokens
        _traverse(item.tokens, tables)
    
    return tables

def _traverse(tokens, tables):
    for token in tokens:
        if isinstance(token, IdentifierList):
            for identifier in token.get_identifiers():
                _extract_table_name(identifier, tables)
        elif isinstance(token, Identifier):
            _extract_table_name(token, tables)
        elif token.is_group:
            _traverse(token.tokens, tables)

def _extract_table_name(token, tables):
    # This function needs to be adapted based on your SQL dialect and query patterns
    if token.ttype is Name or token.ttype is None:
        value = token.get_real_name()
        if value:  # Avoid adding None
            tables.add(value)

def user_has_access(user_tables, query_tables):
    # Convert both sets to lowercase for case-insensitive comparison
    user_tables_lower = {table.lower() for table in user_tables}
    query_tables_lower = {table.lower() for table in query_tables}
    return user_tables_lower.issubset(query_tables_lower)

# Example usage
user_tables = {'employees', 'departments'}  # Tables the user has access to
#query = "SELECT * FROM employees JOIN departments ON employees.dep_id = departments.id"
query="SELECT * FROM (Select * from employees) JOIN departments ON employees.dep_id = departments.id"
query_tables = extract_tables(query)
print(f'Tables the user has access to: {user_tables}')
print(f'Tables in the query: {query_tables}')
if user_has_access(user_tables, query_tables):
    print("User has access to these tables.")
else:
    print("User does not have access to one or more tables in the query.")