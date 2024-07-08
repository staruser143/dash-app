import json
import boto3

def lambda_handler(event, context):
    # Initialize Boto3 Glue client
    glue_client = boto3.client('glue')
    
    database_name = event.get('database_name', 'your_database_name')  # Replace with your database name
    
    try:
        # Fetch the list of tables in the specified database
        response = glue_client.get_tables(DatabaseName=database_name)
        tables = response.get('TableList', [])
        
        table_metadata = []
        
        for table in tables:
            table_name = table['Name']
            table_details = glue_client.get_table(DatabaseName=database_name, Name=table_name)
            table_metadata.append(table_details['Table'])
        
        return {
            'statusCode': 200,
            'body': json.dumps(table_metadata)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
