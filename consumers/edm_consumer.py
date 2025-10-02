# Subscribes to Kafka, processes buzz messages,
# and displays live animated visualization.

import json
import sys
import pathlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import defaultdict
from kafka import KafkaConsumer
from utils.utils_logger import get_logger

# Add project root
PROJECT_ROOT = pathlib.Path(__file__).parent.parent.resolve()
sys.path.append(str(PROJECT_ROOT))

# Configurations
TOPIC_NAME = "buzzline_edm"
BOOTSTRAP_SERVERS = "localhost:9092"
# Initialize logger
logger = get_logger("edm_consumer")

# Kafka Consumer Setup
consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers=BOOTSTRAP_SERVERS,
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

# Data Structure
artist_mentions = defaultdict(int)

# Visualization Setup
fig, ax = plt.subplots(figsize=(8, 6))
plt.title("Live Festival Buzz: Top Artist Mentions", fontsize=14)

def update_chart(frame):
    """
    Update function for Matplotlib animation.
    Reads new Kafka messages, updates counts, and redraws chart.
    """
    # Poll messages from Kafka
    for message in consumer.poll(timeout_ms=100).values():
        for record in message:
            data = record.value
            artist = data.get("artist", "Unknown")
            artist_mentions[artist] += 1
            logger.info(f"Consumed message: {data}")

    # Clear current chart
    ax.clear()

    # Prepare data for bar chart
    if artist_mentions:
        artists = list(artist_mentions.keys())
        counts = list(artist_mentions.values())

        # Sort by most mentions
        sorted_pairs = sorted(zip(artists, counts), key=lambda x: x[1], reverse=True)
        top_artists, top_counts = zip(*sorted_pairs)

        # Plot horizontal bar chart
        ax.barh(top_artists, top_counts, color="skyblue")
        ax.set_xlabel("Mentions")
        ax.set_ylabel("Artist")
        ax.set_title("🎶 Live Festival Buzz: Top Artist Mentions", fontsize=14)

        # Add caption with current leader
        leader = top_artists[0]
        leader_count = top_counts[0]
        ax.text(
            0.95, 0.01,
            f"{leader} leading with {leader_count} mentions",
            transform=ax.transAxes,
            ha="right",
            va="bottom",
            fontsize=10,
            color="darkred",
            weight="bold"
        )
    else:
        ax.text(0.5, 0.5, "Waiting for buzz data...", ha="center", va="center")

# Main
if __name__ == "__main__":
    logger.info("Starting EDM Buzzline consumer...")
    ani = FuncAnimation(fig, update_chart, interval=2000)  # Update every 2s
    plt.show()