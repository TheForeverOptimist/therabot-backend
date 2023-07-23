from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access environment variables
mongodb_url = os.getenv('MONGODB_URL')
port = int(os.getenv('PORT'))

client = MongoClient(mongodb_url)
db = client.therabot_db

collection_name = db["therabot_collection"]