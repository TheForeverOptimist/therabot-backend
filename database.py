from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access environment variables
mongodb_url = os.getenv('MONGODB_URL')
port = int(os.getenv('PORT'))

def connect_to_mongodb():
    try:
        # Connect to MongoDB
        client = MongoClient(mongodb_url, port=port)
        db = client["therabot"]
        print("Successfully connected to MongoDB")
        return db
    except Exception as e:
        print("Failed to connect to MongoDB:", str(e))
