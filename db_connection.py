from pymongo import MongoClient


    # Replace <db_password> with your password and <database> with your database name
CONNECTION_STRING = "mongodb+srv://ehte71:admin@cluster0.r3wmk.mongodb.net/<cluster0>?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)


db = client['assignment2']


