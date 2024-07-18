# import os
# from pymongo import mongo_client
# from dotenv import load_dotenv

# load_dotenv()

# MONGO_DB_CONNECTION_URL = os.environ.get('MONGO_DB_CONNECTION_URL')

# client = mongo_client.MongoClient(MONGO_DB_CONNECTION_URL)
# print("Connected to MongoDB")

# # Get or create collection
# books_collection = client["book_app"]["books"]
# users_collection = client["book_app"]["users"]


import os
from pymongo import mongo_client
from dotenv import load_dotenv

load_dotenv()

MONGO_DBCONNECTION_URL = os.environ.get('MONGO_DBCONNECTION_URL')

client = mongo_client.MongoClient(MONGO_DBCONNECTION_URL)
print("Connected to MongoDB")

# create collection
books_collection = client["book_app"]["books"]

users_collection = client["book_app"]["users"]