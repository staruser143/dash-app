
import sqlite3

# Connect to the database
connection = sqlite3.connect('my_database.db')

# Create a cursor
cursor = connection.cursor()

# Execute a DELETE statement
cursor.execute("DELETE FROM user_table_access")
# Commit the changes
connection.commit()