# Generates live-streamed JSON messages about
# festival buzz and sends them to Kafka.

import json
import time
import sys
import pathlib
from kafka import KafkaProducer
from utils.utils_logger import get_logger
from utils.utils_data import generate_message

# Add project root to sys.path
PROJECT_ROOT = pathlib.Path(__file__).parent.parent.resolve()
sys.path.append(str(PROJECT_ROOT))

# Configurations
TOPIC_NAME = "buzzline_edm"
BOOTSTRAP_SERVERS = "localhost:9092"
SLEEP_INTERVAL = 2   # Seconds between messages
# Initialize logger
logger = get_logger("edm_producer")

# Kafka Producer Setup
producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# Producer Loop
def run_producer():
    logger.info("Starting EDM Buzzline producer...")
    try:
        while True:
            # Generate a buzz message
            message = generate_message()
            
            # Send to Kafka
            producer.send(TOPIC_NAME, value=message)
            producer.flush()

            logger.info(f"Produced message: {message}")

            # Wait before sending next message
            time.sleep(SLEEP_INTERVAL)

    except KeyboardInterrupt:
        logger.info("Producer stopped by user.")
    except Exception as e:
        logger.error(f"Producer error: {e}")
    finally:
        producer.close()
        logger.info("Kafka producer closed.")


if __name__ == "__main__":
    run_producer()
