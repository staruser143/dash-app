def authenticate_user(username, password):
    token = get_valid_access_token()
    response = requests.post(DIRECTORY_SERVICE_AUTH_URL, json={
        'username': username,
        'password': password
    }, headers={
        'Authorization': f'Bearer {token}'
    })

    if response.status_code == 200:
        return response.json()  # Return user authentication response
    else:
        return None
