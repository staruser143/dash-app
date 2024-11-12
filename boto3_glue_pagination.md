Yes, AWS Boto3 Glue supports fetching a list of tables in a paginated manner using the get_tables() method with pagination. You can use a paginator to handle larger datasets efficiently.

Here’s an example:

import boto3

client = boto3.client('glue')
paginator = client.get_paginator('get_tables')

database_name = 'your_database_name'
tables = []

for page in paginator.paginate(DatabaseName=database_name):
    tables.extend(page['TableList'])

print(f"Total tables: {len(tables)}")
for table in tables:
    print(table['Name'])

This code initializes a paginator for get_tables and iterates over each page to collect all tables in the specified database, which allows you to handle paginated results without manually managing pagination tokens.

