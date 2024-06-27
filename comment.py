import psycopg2

def add_comments_to_table_and_columns(dbname, user, password, host, table_name, table_comment, column_comments):
    """
    Adds comments to a table and its columns in a PostgreSQL database.

    Parameters:
    - dbname: Database name
    - user: Username
    - password: Password
    - host: Host address
    - table_name: Name of the table to comment
    - table_comment: Comment for the table
    - column_comments: Dictionary of column names and their comments
    """
    try:
        # Connect to the database
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
        cur = conn.cursor()

        # Add comment to the table
        cur.execute(f"COMMENT ON TABLE {table_name} IS %s;", (table_comment,))

        # Add comments to columns
        for column, comment in column_comments.items():
            cur.execute(f"COMMENT ON COLUMN {table_name}.{column} IS %s;", (comment,))

        # Commit the changes
        conn.commit()

        print("Comments added successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the cursor and connection
        if cur:
            cur.close()
        if conn:
            conn.close()

# Example usage
dbname = 'mydatabase'
user = 'postgres'
password = 'mysecretpassword'
host = 'localhost'
table_name = 'your_table_name'
table_comment = 'This is the table comment.'
column_comments = {
    'column1': 'Comment for column1',
    'column2': 'Comment for column2',
    # Add more columns as needed
}

add_comments_to_table_and_columns(dbname, user, password, host, table_name, table_comment, column_comments)