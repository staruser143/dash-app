import psycopg2

# Step 3: Connect to the PostgreSQL database
conn = psycopg2.connect(
    dbname='mydatabase', 
    user='postgres', 
    password='mysecretpassword', 
    host='localhost', 
    port='5432'  # Default PostgreSQL port is 5432\c mydatabase
)

try:
    # Step 4: Create a cursor object
    cursor = conn.cursor()
    
    cursor.execute("CREATE TABLE IF NOT EXISTS transactions (id serial PRIMARY KEY, name VARCHAR(100))")
    #Add comment to table transactions
    cursor.execute("COMMENT ON TABLE transactions IS 'Stores transaction records'")
    #Add comment to column id
    cursor.execute("COMMENT ON COLUMN transactions.id IS 'Unique identifier for the transaction'")  
    #Add comment to column name 
    cursor.execute("COMMENT ON COLUMN transactions.name IS 'Name of the transaction'")
    
    # insert 100 rows of mock data into table tranactions
    mock_data = []
    for i in range(1, 101):
        name = f"Transaction {i}"
        mock_data.append((name,))
    # Insert mock data into the table
    cursor.executemany("INSERT INTO transactions (name) VALUES (%s)", mock_data)

    # Step 5: Execute a query
    cursor.execute("SELECT * FROM transactions")
    
    # Fetch and print the result of the query
    records = cursor.fetchall()
    for record in records:
        print(record)
    
    # Commit the transaction (if needed)
    conn.commit()
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Step 6: Close the cursor and connection
    cursor.close()
    conn.close()