from flask import Flask, request, jsonify
import random
import string
import secrets  # Improved key generation method

app = Flask(__name__)

# Store users and their keys
user_verified = {}

# Generate a secure unique key
def generate_key():
    return secrets.token_urlsafe(16)  # Cryptographically secure key generation

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'  # Allow all origins, or set your specific domain
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
    return response

@app.route('/generate_key', methods=['POST'])
def generate_verification_key():
    data = request.json
    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    
    key = generate_key()
    user_verified[user_id] = key
    
    return jsonify({'key': key}), 200

@app.route('/verify_key', methods=['POST'])
def verify_key():
    data = request.json
    user_id = data.get('user_id')
    key = data.get('key')
    
    if not user_id or not key:
        return jsonify({'error': 'Both user_id and key are required'}), 400
    
    if user_verified.get(user_id) == key:
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False}), 400

if __name__ == '__main__':
    app.run(debug=True)
