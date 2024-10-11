import os
from pymongo import MongoClient
from dotenv import load_dotenv
from loguru import logger

# Load environment variables
load_dotenv()

# MongoDB Configuration
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
MONGODB_DB = os.getenv('MONGODB_DB', 'customer_behavior_db')
MONGODB_COLLECTION = os.getenv('MONGODB_COLLECTION', 'events')

# Initialize MongoDB Client
client = MongoClient(MONGODB_URI)
db = client[MONGODB_DB]
collection = db[MONGODB_COLLECTION]

# Configure Logging
logger.add("setup_db.log", rotation="10 MB")

def setup_indexes():
    try:
        collection.create_index([('customer_id', 1)])
        collection.create_index([('event_type', 1)])
        collection.create_index([('timestamp', 1)])
        logger.info("MongoDB indexes created successfully.")
    except Exception as e:
        logger.error(f"Error creating indexes: {e}")
    finally:
        client.close()
        logger.info("MongoDB connection closed.")

if __name__ == "__main__":
    setup_indexes()

