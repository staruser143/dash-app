def fetch_user_details(user_id):
    token = get_valid_access_token()
    response = requests.get(f'{DIRECTORY_SERVICE_SEARCH_URL}/{user_id}', headers={
        'Authorization': f'Bearer {token}'
    })

    if response.status_code == 200:
        return response.json()  # Return user details
    else:
        return None
