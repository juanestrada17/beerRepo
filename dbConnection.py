import os
from pymongo import MongoClient
from dotenv import load_dotenv


def start_db_connection():
    try:
        load_dotenv()
        mongo_uri = os.getenv('MONGO_URI')
        db_name = os.getenv('MONGO_DB_NAME')
        collection_name = os.getenv('MONGO_COLLECTION_NAME')

        client = MongoClient(mongo_uri)
        db = client[db_name]
        collection = db[collection_name]

        return db, collection
    except Exception as e:
        print(f"Can't connect to db: {e}")
