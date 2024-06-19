from sqlalchemy import create_engine,text

# Create an engine that uses a connection pool
engine = create_engine('sqlite:///my_database.db', pool_size=10, max_overflow=20)

# Get a connection from the pool
connection = engine.connect()

name = 'John Doe'  # This should come from your application
# Execute a query
query = text("SELECT * FROM employees WHERE name = :name")

result = connection.execute(query, {'name': name})

# Fetch all rows
rows = result.fetchall()

# Print each row
for row in rows:
    print(row)

# Close the connection (returns it to the pool)
connection.close()