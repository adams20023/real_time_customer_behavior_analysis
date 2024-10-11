import time
import json
import os
from kafka import KafkaProducer
from faker import Faker
from dotenv import load_dotenv
import random
import logging

# Load environment variables
load_dotenv()

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("producer.log"),
        logging.StreamHandler()
    ]
)

fake = Faker()

# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'customer_behavior')
PRODUCER_SLEEP_INTERVAL = float(os.getenv('PRODUCER_SLEEP_INTERVAL', 1))

producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def generate_customer_behavior():
    return {
        "customer_id": fake.uuid4(),
        "event_type": random.choice(["page_view", "add_to_cart", "purchase", "login", "logout"]),
        "timestamp": int(time.time()),
        "page": fake.uri_path(),
        "product_id": fake.uuid4(),
        "price": round(random.uniform(10.0, 500.0), 2)
    }

if __name__ == "__main__":
    try:
        while True:
            message = generate_customer_behavior()
            producer.send(KAFKA_TOPIC, value=message)
            logging.info(f"Produced message: {message}")
            time.sleep(PRODUCER_SLEEP_INTERVAL)
    except KeyboardInterrupt:
        logging.info("Stopping producer")
    finally:
        producer.close()

