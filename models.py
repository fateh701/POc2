from db import db

users_collection = db['User']

# Create a new user
def create_user(user_data):
    result = users_collection.insert_one(user_data)
    return str(result.inserted_id)

# Get all users
def get_all_users():
    return list(users_collection.find({}, {"_id": 0}))

# Update user details
def update_user(user_id, updates):
    result = users_collection.update_one({"user_id": user_id}, {"$set": updates})
    return result.matched_count > 0

# Get user by ID
def get_user_by_id(user_id):
    return users_collection.find_one({"user_id": user_id}, {"_id": 0})
