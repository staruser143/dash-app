from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import redshift_connector

# Define the connection string
# Format: redshift+redshift_connector://username:password@hostname:port/database
connection_string = "redshift+redshift_connector://myuser:mypassword@myhost:5439/mydatabase"

# Create the engine
engine = create_engine(connection_string)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a session
session = Session()



from sqlalchemy import text

# Assume you have a session object from the previous steps
# session = Session()

# Define your SQL query
sql_query = "SELECT * FROM my_table WHERE my_column = :value"

# Execute the query
result = session.execute(text(sql_query), {'value': 'some value'})

# Fetch all rows from the result (if you expect multiple rows)
rows = result.fetchall()

# Or fetch one row (if you expect one row)
row = result.fetchone()

# Don't forget to close the session when you're done
session.close()