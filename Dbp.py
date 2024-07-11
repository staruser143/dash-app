with conn.cursor() as cursor:
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        sale_id INT PRIMARY KEY,
        product_name VARCHAR(255),
        sale_amount DECIMAL(10, 2),
        sale_date DATE
    )
    """)
