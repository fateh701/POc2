from flask import Flask, request, jsonify
from models import create_user, get_all_users, update_user, get_user_by_id

app = Flask(__name__)

# Route to create a new user
@app.route('/v2/users', methods=['POST'])
def create_user_endpoint():
    data = request.json
    if not data or 'user_id' not in data or 'email' not in data or 'delivery_address' not in data:
        return jsonify({"error": "Invalid input"}), 400

    user_data = {
        "user_id": data["user_id"],
        "email": data["email"],
        "delivery_address": data["delivery_address"]
    }
    user_id = create_user(user_data)
    return jsonify({"message": "User created", "user_id": user_id}), 201

# Route to fetch all users
@app.route('/v2/users', methods=['GET'])
def get_users_endpoint():
    users = get_all_users()
    return jsonify(users), 200

# Route to update user details
@app.route('/v2/users/<user_id>', methods=['PUT'])
def update_user_endpoint(user_id):
    data = request.json
    if not data:
        return jsonify({"error": "Invalid input"}), 400

    updates = {}
    if "email" in data:
        updates["email"] = data["email"]
    if "delivery_address" in data:
        updates["delivery_address"] = data["delivery_address"]

    updated = update_user(user_id, updates)
    if not updated:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"message": "User updated successfully"}), 200

# Route to fetch a single user by ID
@app.route('/v2/users/<user_id>', methods=['GET'])
def get_user_endpoint(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user), 200

if __name__ == '__main__':
    app.run(host="127.0.0.1", debug=True, port=5002)
