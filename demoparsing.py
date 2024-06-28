import sqlparse
from sqlparse.sql import IdentifierList, Identifier
from sqlparse.tokens import Keyword, DML

# Parse an SQL query
query = "SELECT * FROM employees JOIN departments ON employees.dep_id = departments.id"
parsed = sqlparse.parse(query)

# `parsed` is a tuple of statements (even if there's only one)
statement = parsed[0]

# Iterate over tokens in the statement
for token in statement.tokens:
    if token.ttype is DML:  # DML (Data Manipulation Language) tokens, e.g., SELECT
        print("DML found:", token)
    if token.ttype is Keyword:  # SQL Keywords, e.g., FROM, JOIN
        print("Keyword found:", token)
    if isinstance(token, IdentifierList) or isinstance(token, Identifier):
        print("Identifier found:", token)