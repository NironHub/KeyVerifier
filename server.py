from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import string

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests (e.g., from Roblox)

keys = {}  # Stores keys by user_id

def generate_key():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))

@app.route('/')
def home():
    return "✅ Flask server is running."

@app.route('/generate_key', methods=['POST'])
def generate_key_route():
    data = request.get_json()
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    key = generate_key()
    keys[user_id] = key
    print(f"[KEY GENERATED] {user_id} -> {key}")
    return jsonify({"key": key}), 200

@app.route('/verify_key', methods=['POST'])
def verify_key_route():
    data = request.get_json()
    user_id = data.get("user_id")
    key = data.get("key")

    if not user_id or not key:
        return jsonify({"error": "Missing user_id or key"}), 400

    if keys.get(user_id) == key:
        del keys[user_id]  # Optional: remove used key
        print(f"[VERIFIED] {user_id} with key {key}")
        return jsonify({"success": True}), 200
    else:
        print(f"[FAILED] {user_id} tried invalid key {key}")
        return jsonify({"success": False, "message": "Invalid key"}), 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
