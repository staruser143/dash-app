import sqlite3

# Connect to the database
connection = sqlite3.connect('my_database.db')

# Create a cursor
cursor = connection.cursor()

# Assume `name` is a variable holding the user-provided input
name = 'John Doe'  # This should come from your application

# Correct way: Use a placeholder and provide the value as a tuple
cursor.execute("SELECT * FROM employees WHERE name = ?", (name,))


# Fetch all records
records = cursor.fetchall()

# Print each record
for record in records:
    print(record)

# Close the connection
connection.close()