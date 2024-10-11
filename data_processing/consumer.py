import os
import json
from kafka import KafkaConsumer
from pymongo import MongoClient
from dotenv import load_dotenv
from loguru import logger
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure Logging
logger.add("consumer.log", rotation="10 MB")

# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'customer_behavior')
KAFKA_GROUP_ID = os.getenv('KAFKA_GROUP_ID', 'customer_behavior_group')

# MongoDB Configuration
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
MONGODB_DB = os.getenv('MONGODB_DB', 'customer_behavior_db')
MONGODB_COLLECTION = os.getenv('MONGODB_COLLECTION', 'events')

# Initialize MongoDB Client
client = MongoClient(MONGODB_URI)
db = client[MONGODB_DB]
collection = db[MONGODB_COLLECTION]

# Initialize Kafka Consumer
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id=KAFKA_GROUP_ID,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Ensure Indexes are Created
def create_indexes():
    collection.create_index([('customer_id', 1)])
    collection.create_index([('event_type', 1)])
    collection.create_index([('timestamp', 1)])
    logger.info("MongoDB indexes created successfully.")

if __name__ == "__main__":
    create_indexes()
    logger.info("Starting consumer...")
    try:
        for message in consumer:
            event = message.value
            # Add processed timestamp
            event['processed_at'] = int(datetime.utcnow().timestamp())
            # Insert into MongoDB
            collection.insert_one(event)
            logger.info(f"Inserted event: {event}")
    except KeyboardInterrupt:
        logger.info("Stopping consumer")
    except Exception as e:
        logger.error(f"Error occurred: {e}")
    finally:
        consumer.close()
        client.close()
        logger.info("Consumer closed.")

