from models import create_user

# Add test data
create_user(user_id="u001", email="user1@example.com", delivery_address="123 Main St")
"""
create_order(order_id="o001", items=["item1", "item2"], email="user1@example.com", delivery_address="123 Main St")"""

print("Test data inserted successfully.")
