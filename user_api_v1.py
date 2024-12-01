from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

# MongoDB connection
CONNECTION_STRING = os.getenv("MONGO_URI", "mongodb+srv://ehte71:admin@cluster0.r3wmk.mongodb.net/assignment2?retryWrites=true&w=majority&tls=true")
client = MongoClient(CONNECTION_STRING)
db = client['assignment2']
users_collection = db['User']

# Endpoint to create a new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    if not data or 'user_id' not in data or 'email' not in data or 'delivery_address' not in data:
        return jsonify({"error": "Invalid input"}), 400

    user = {
        "user_id": data["user_id"],
        "email": data["email"],
        "delivery_address": data["delivery_address"]
    }
    result = users_collection.insert_one(user)
    return jsonify({"message": "User created", "user_id": str(result.inserted_id)}), 201

# Endpoint to fetch all users
@app.route('/users', methods=['GET'])
def get_users():
    users = list(users_collection.find({}, {"_id": 0}))
    return jsonify(users), 200

# Endpoint to fetch a single user by ID
@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = users_collection.find_one({"user_id": user_id}, {"_id": 0})
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user), 200

# Endpoint to update a user's email or delivery address
@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    if not data:
        return jsonify({"error": "Invalid input"}), 400

    updates = {}
    if "email" in data:
        updates["email"] = data["email"]
    if "delivery_address" in data:
        updates["delivery_address"] = data["delivery_address"]

    result = users_collection.update_one({"user_id": user_id}, {"$set": updates})
    if result.matched_count == 0:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "User updated successfully"}), 200

# Endpoint to delete a user
@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = users_collection.delete_one({"user_id": user_id})
    if result.deleted_count == 0:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "User deleted successfully"}), 200

if __name__ == '__main__':
    app.run(host="127.0.0.1", debug=True, port=5000)
