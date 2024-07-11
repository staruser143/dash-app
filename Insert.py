import redshift_connector

# Connect to Redshift
conn = redshift_connector.connect(
    user='your_user',
    password='your_password',
    database='your_database',
    host='your_cluster_endpoint',
    port=5439
)

# Create a cursor object
cursor = conn.cursor()

# Insert records
insert_query = """
INSERT INTO sales (product_name, sale_amount, sale_date)
VALUES (%s, %s, %s)
"""

data = [
    ('Product A', 100.00, '2024-07-01'),
    ('Product B', 150.00, '2024-07-02')
]

cursor.executemany(insert_query, data)

# Commit the transaction
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()
