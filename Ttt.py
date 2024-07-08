import json
import boto3
from datetime import datetime

def lambda_handler(event, context):
    glue_client = boto3.client('glue')
    database_name = event.get('queryStringParameters', {}).get('database_name', 'your_database_name')  # Default to 'your_database_name' if not provided

    def convert_datetime(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError("Type not serializable")

    try:
        response = glue_client.get_tables(DatabaseName=database_name)
        tables = response.get('TableList', [])
        
        table_metadata = []
        
        for table in tables:
            table_name = table['Name']
            table_details = glue_client.get_table(DatabaseName=database_name, Name=table_name)
            table_metadata.append(table_details['Table'])
        
        return {
            'statusCode': 200,
            'body': json.dumps(table_metadata, default=convert_datetime)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
