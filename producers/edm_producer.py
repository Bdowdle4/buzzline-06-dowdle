# Streams buzz messages into Kafka and 
# writes them to edm_live.json for backup/testing.

import json
import time
import sys
import pathlib
import random
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

DATA_FOLDER = PROJECT_ROOT.joinpath("data")
DATA_FOLDER.mkdir(exist_ok=True)
DATA_FILE = DATA_FOLDER.joinpath("edm_live.json")

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
    # Reset local file each run
    with open(DATA_FILE, "w") as f:
        f.write("")

    try:
        while True:
            # Generate random buzz message
            message = generate_message()

            # Send to Kafka
            producer.send(TOPIC_NAME, value=message)

            # Append to local JSON file
            with open(DATA_FILE, "a") as f:
                f.write(json.dumps(message) + "\n")

            logger.info(f"Produced: {message}")

            # Sleep for a short random interval to simulate "live" buzz
            time.sleep(random.uniform(0.5, 2.0))

    except KeyboardInterrupt:
        logger.info("Producer stopped by user.")
    finally:
        producer.flush()
        producer.close()

# Main
if __name__ == "__main__":
    run_producer()