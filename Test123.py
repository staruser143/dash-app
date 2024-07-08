def lambda_handler(event, context):
    # Entry point for the Lambda function
    path = event.get('path', '/')
    http_method = event.get('httpMethod', 'GET')
    
    if path == '/resource1' and http_method == 'GET':
        return handle_get_resource1(event)
    elif path == '/resource2' and http_method == 'POST':
        return handle_post_resource2(event)
    else:
        return {
            'statusCode': 404,
            'body': 'Not Found'
        }

def handle_get_resource1(event):
    query_params = event.get('queryStringParameters', {})
    param_value = query_params.get('param_name', 'default_value')
    return {
        'statusCode': 200,
        'body': f'GET Resource1 - Value of param_name is {param_value}'
    }

def handle_post_resource2(event):
    body = event.get('body', '{}')
    # Process the POST data
    return {
        'statusCode': 200,
        'body': f'POST Resource2 - Body is {body}'
    }
