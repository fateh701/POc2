import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://ehte71:admin@cluster0.r3wmk.mongodb.net/assignment2?retryWrites=true&w=majority&tls=true")
DATABASE_NAME = os.getenv("DATABASE_NAME", "assignment2")
