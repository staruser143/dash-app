import sqlite3
import random
from faker import Faker

# Create an instance of the Faker class
fake = Faker()

# Connect to the database
connection = sqlite3.connect('my_database.db')

# Create a cursor
cursor = connection.cursor()

# Execute a SQL command
cursor.execute("DROP TABLE IF EXISTS employees")
cursor.execute('CREATE TABLE IF NOT EXISTS employees (id integer primary key, name text, position text, office text)')

# Create a table Department with columns id integer primary key, name text, managername text
cursor.execute("DROP TABLE IF EXISTS department")
cursor.execute('CREATE TABLE IF NOT EXISTS department (id integer primary key, name text, managername text)')

# Insert a row of data
cursor.execute("DELETE FROM employees")
# Insert 1000 rows of fake data in a loop with id starting from 1
# Generate mock data
mock_data = []
for i in range(1, 5):
    name = fake.name()
    position = random.choice(["Manager", "AVP", "Secretary"])
    office = random.choice(["Head Office", "East Office", "West Office"])
    mock_data.append((i, name, position, office))

# Insert mock data into the table
cursor.executemany("INSERT INTO employees (id, name, position, office) VALUES (?, ?, ?, ?)", mock_data)
#cursor.execute("INSERT INTO employees VALUES ('Khan kumar','AVP','Head Office')")
#cursor.execute("INSERT INTO employees VALUES ('Sangeetha Doe','SEcratary','Head Office')")
# Save (commit) the changes
connection.commit()

# Close the connection
connection.close()