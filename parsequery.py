import demoparsing
from sqlparse.sql import IdentifierList, Identifier
from sqlparse.tokens import Name, Whitespace, Wildcard

def extract_tables(sql):
    # Parse the SQL query
    parsed = demoparsing.parse(sql)
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
    return query_tables.issubset(user_tables)

# Example usage
user_tables = {'employees', 'departments'}  # Tables the user has access to
query = "SELECT * FROM employees JOIN departments ON employees.dep_id = departments.id"

query_tables = extract_tables(query)

if user_has_access(user_tables, query_tables):
    print("User has access to these tables.")
else:
    print("User does not have access to one or more tables in the query.")