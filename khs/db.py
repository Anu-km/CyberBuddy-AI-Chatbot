from pymongo import MongoClient
import os

client = MongoClient(os.getenv("MONGO_URI"))
db = client.cyberbuddy
users = db.users
chats = db.chats
