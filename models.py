from db_connection import db

# User schema
user_collection = db['User']
def create_user(user_id, email, delivery_address):
    user = {
        "user_id": user_id,
        "email": email,
        "delivery_address": delivery_address
    }
    user_collection.insert_one(user)

# Order schema

"""order_collection = db['orders']
def create_order(order_id, items, email, delivery_address, status="under process"):
    order = {
        "order_id": order_id,
        "items": items,
        "email": email,
        "delivery_address": delivery_address,
        "status": status
    }
    order_collection.insert_one(order)
"""