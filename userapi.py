import pika
from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
CONNECTION_STRING = "mongodb+srv://ehte71:admin@cluster0.r3wmk.mongodb.net/myDatabase?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)
db = client['assignment2']
users_collection = db['User']

# RabbitMQ connection
rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = rabbitmq_connection.channel()
channel.exchange_declare(exchange='user_events', exchange_type='fanout')

# Function to send RabbitMQ message
def send_event(event):
    channel.basic_publish(exchange='user_events', routing_key='', body=event)

# Endpoint to update a user's email or delivery address
@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    update_fields = {}
    if "email" in data:
        update_fields["email"] = data["email"]
    if "delivery_address" in data:
        update_fields["delivery_address"] = data["delivery_address"]

    result = users_collection.update_one({"user_id": user_id}, {"$set": update_fields})
    if result.matched_count == 0:
        return jsonify({"error": "User not found"}), 404

    # Send event to RabbitMQ
    event = {
        "user_id": user_id,
        "email": update_fields.get("email"),
        "delivery_address": update_fields.get("delivery_address")
    }
    send_event(str(event))

    return jsonify({"message": "User updated successfully"}), 200

if __name__ == '__main__':
    app.run(host="127.0.0.1", debug=True, port=5000)
