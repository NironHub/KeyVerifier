from flask import Flask, request, jsonify
import random
import string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Store users and their keys
user_verified = {}

# Generate a unique key
def generate_key():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))

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
    
    if user_verified.get(user_id) == key:
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False}), 400

if __name__ == '__main__':
    app.run(debug=True)
