
import sqlite3

# Connect to the database
connection = sqlite3.connect('my_database.db')

# Create a cursor
cursor = connection.cursor()

# Execute a SELECT statement
cursor.execute("SELECT * FROM Users")

# Fetch all records
records = cursor.fetchall()

# Print each record
for record in records:
    print(record)

# Close the connection
connection.close()