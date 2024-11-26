import pika
import json
from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
CONNECTION_STRING = "mongodb+srv://ehte71:admin@cluster0.r3wmk.mongodb.net/myDatabase?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)
db = client['assignment2']
orders_collection = db['orders']

# RabbitMQ connection
rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = rabbitmq_connection.channel()
channel.exchange_declare(exchange='user_events', exchange_type='fanout')

# Function to update orders when user data changes
def update_orders(ch, method, properties, body):
    event = json.loads(body)
    user_id = event.get("user_id")
    email = event.get("email")
    delivery_address = event.get("delivery_address")

    update_fields = {}
    if email:
        update_fields["email"] = email
    if delivery_address:
        update_fields["delivery_address"] = delivery_address

    # Update orders in the database
    result = orders_collection.update_many({"user_id": user_id}, {"$set": update_fields})
    print(f"Updated {result.modified_count} orders for user {user_id}")

# RabbitMQ consumer setup
channel.queue_declare(queue='', exclusive=True)
queue_name = channel.queue_declare(queue='', exclusive=True).method.queue
channel.queue_bind(exchange='user_events', queue=queue_name)
channel.basic_consume(queue=queue_name, on_message_callback=update_orders, auto_ack=True)

# Start RabbitMQ consumer in a separate thread
import threading
def start_rabbitmq_consumer():
    print("Starting RabbitMQ consumer...")
    channel.start_consuming()

threading.Thread(target=start_rabbitmq_consumer, daemon=True).start()

# Existing order API endpoints...
@app.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    order = {
        "order_id": data.get("order_id"),
        "user_id": data.get("user_id"),
        "items": data.get("items"),
        "email": data.get("email"),
        "delivery_address": data.get("delivery_address"),
        "status": data.get("status", "under process")
    }
    result = orders_collection.insert_one(order)
    return jsonify({"message": "Order created", "order_id": str(result.inserted_id)}), 201

if __name__ == '__main__':
    app.run(host="127.0.0.1", debug=True, port=5001)
