import requests
from datetime import datetime, timedelta
from threading import Timer

# Configuration
CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'
AUTHORIZATION_SERVER_TOKEN_URL = 'https://your-authorization-server.com/oauth/token'
DIRECTORY_SERVICE_AUTH_URL = 'https://your-directory-service.com/api/authenticate'
DIRECTORY_SERVICE_SEARCH_URL = 'https://your-directory-service.com/api/search'

# Token storage
access_token = None
token_expiry = None

def get_access_token():
    global access_token, token_expiry

    response = requests.post(AUTHORIZATION_SERVER_TOKEN_URL, data={
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    })
    
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data['access_token']
        expires_in = token_data['expires_in']
        token_expiry = datetime.now() + timedelta(seconds=expires_in)
    else:
        raise Exception("Failed to obtain access token from authorization server")

def is_token_expired():
    if token_expiry is None:
        return True
    return datetime.now() >= token_expiry

def get_valid_access_token():
    if is_token_expired():
        get_access_token()
    return access_token

def renew_token():
    try:
        get_access_token()
    except Exception as e:
        print(f"Error renewing token: {e}")
    finally:
        # Set timer to renew token before it expires
        Timer(token_expiry - datetime.now() - timedelta(minutes=5), renew_token).start()

# Initialize token and start periodic renewal
get_access_token()
renew_token()
