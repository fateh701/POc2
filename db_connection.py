from pymongo import MongoClient


    # Replace <db_password> with your password and <database> with your database name
CONNECTION_STRING = "mongodb+srv://ehte71:admin@cluster0.r3wmk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(CONNECTION_STRING)


db = client['assignment2']


