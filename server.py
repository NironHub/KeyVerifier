from flask import Flask, request, jsonify
import secrets
import logging
import os
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS with restricted origins (set as an environment variable)
CORS(app, origins=os.getenv('ALLOWED_ORIGIN', '*'), supports_credentials=True)

# Store users and their keys
user_verified = {}

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Generate a secure unique key
def generate_key():
    return secrets.token_urlsafe(32)  # Stronger key length

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
    return response

@app.route('/generate_key', methods=['POST'])
def generate_verification_key():
    data = request.json
    user_id = data.get('user_id')

    if not user_id:
        logger.error("User ID is missing in the request.")
        return jsonify({'error': 'User ID is required'}), 400
    
    # Generate the key and store it
    key = generate_key()
    user_verified[user_id] = key

    logger.info(f"Generated key for user_id {user_id}")
    return jsonify({'key': key}), 200

@app.route('/verify_key', methods=['POST'])
def verify_key():
    data = request.json
    user_id = data.get('user_id')
    key = data.get('key')

    if not user_id or not key:
        logger.error("Missing user_id or key in the request.")
        return jsonify({'error': 'Both user_id and key are required'}), 400
    
    stored_key = user_verified.get(user_id)
    if not stored_key:
        logger.warning(f"User ID {user_id} not found.")
        return jsonify({'error': 'User not found'}), 404
    
    if stored_key == key:
        logger.info(f"User ID {user_id} successfully verified.")
        return jsonify({'success': True}), 200
    else:
        logger.warning(f"Failed verification for user_id {user_id}. Invalid key.")
        return jsonify({'success': False, 'error': 'Invalid key'}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
