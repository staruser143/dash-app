from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

# Store the client credentials and token data
CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'
TOKENS = {}

@app.route('/oauth/token', methods=['POST'])
def token():
    client_id = request.form.get('client_id')
    client_secret = request.form.get('client_secret')

    if client_id == CLIENT_ID and client_secret == CLIENT_SECRET:
        access_token = 'mock_access_token'
        expires_in = 3600  # 1 hour
        token_data = {
            'access_token': access_token,
            'expires_in': expires_in,
            'expiry_time': datetime.utcnow() + timedelta(seconds=expires_in)
        }
        TOKENS[access_token] = token_data
        return jsonify(token_data)
    else:
        return jsonify({'error': 'invalid_client'}), 401

@app.route('/validate_token', methods=['GET'])
def validate_token():
    token = request.headers.get('Authorization').split()[1]
    if token in TOKENS and TOKENS[token]['expiry_time'] > datetime.utcnow():
        return jsonify({'valid': True})
    else:
        return jsonify({'valid': False}), 401

if __name__ == '__main__':
    app.run(port=5000)
