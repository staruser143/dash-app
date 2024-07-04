from flask import Flask, request, jsonify

app = Flask(__name__)

# Mock users data
USERS = {
    'user1': {'username': 'user1', 'password': 'pass1', 'user_id': '1', 'name': 'User One'},
    'user2': {'username': 'user2', 'password': 'pass2', 'user_id': '2', 'name': 'User Two'}
}

@app.route('/api/authenticate', methods=['POST'])
def authenticate():
    token = request.headers.get('Authorization').split()[1]
    if token != 'mock_access_token':
        return jsonify({'error': 'invalid_token'}), 401

    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = USERS.get(username)
    if user and user['password'] == password:
        return jsonify({'user_id': user['user_id']})
    else:
        return jsonify({'error': 'invalid_credentials'}), 401

@app.route('/api/search/<user_id>', methods=['GET'])
def search(user_id):
    token = request.headers.get('Authorization').split()[1]
    if token != 'mock_access_token':
        return jsonify({'error': 'invalid_token'}), 401

    for user in USERS.values():
        if user['user_id'] == user_id:
            return jsonify(user)
    return jsonify({'error': 'user_not_found'}), 404

if __name__ == '__main__':
    app.run(port=5001)
