
import sqlite3

# Connect to the database
connection = sqlite3.connect('my_database.db')

# Create a cursor
cursor = connection.cursor()

# Execute an UPDATE statement
cursor.execute("UPDATE employees SET position = 'CEO' WHERE name = 'John Doe'")

# Commit the changes
connection.commit()