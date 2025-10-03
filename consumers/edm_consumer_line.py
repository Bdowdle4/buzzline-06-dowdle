# Subscribes to Kafka, processes buzz messages,logs them locally, 
# and displays live animated line chart of stage buzz.

import json
import pathlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import defaultdict, deque
from kafka import KafkaConsumer
import itertools
from utils.utils_logger import get_logger

# Configurations
TOPIC_NAME = "buzzline_edm"
BOOTSTRAP_SERVERS = "localhost:9092"

PROJECT_ROOT = pathlib.Path(__file__).parent.parent.resolve()
DATA_FOLDER = PROJECT_ROOT.joinpath("data")
DATA_FOLDER.mkdir(exist_ok=True)
DATA_FILE = DATA_FOLDER.joinpath("edm_live.json")

# Initialize logger
logger = get_logger("edm_consumer_line")

# Kafka Consumer Setup
consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers=BOOTSTRAP_SERVERS,
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

# Data Structures
# Keep last N time points for visualization
MAX_POINTS = 20

# Dictionary: stage -> deque of counts
stage_counts = defaultdict(lambda: deque(maxlen=MAX_POINTS))

# Global time step counter (acts like x-axis ticks)
time_index = itertools.count()

# Visualization Setup
fig, ax = plt.subplots(figsize=(10, 6))
plt.title("Live Festival Buzz: Stage Mentions Over Time", fontsize=14)

def update_chart(frame):
    """
    Update function for Matplotlib animation.
    Reads new Kafka messages, updates counts, logs to file, and redraws line chart.
    """
    global stage_counts

    # Poll Kafka for new messages
    new_counts = defaultdict(int)
    records = consumer.poll(timeout_ms=100)

    for partition_batch in records.values():
        for record in partition_batch:
            data = record.value
            stage = data.get("stage", "Unknown")
            new_counts[stage] += 1

            # Log to console
            logger.info(f"Consumed message: {data}")

            # Append to local file
            with open(DATA_FILE, "a") as f:
                f.write(json.dumps(data) + "\n")

    # Advance time step
    t = next(time_index)

    # Update each stage deque
    for stage in stage_counts.keys() | new_counts.keys():
        stage_counts[stage].append(new_counts.get(stage, 0))

    # Clear plot
    ax.clear()

    # Draw one line per stage
    for stage, counts in stage_counts.items():
        ax.plot(range(len(counts)), counts, marker="o", label=stage)

    ax.set_xlabel("Time (updates)")
    ax.set_ylabel("Mentions per interval")
    ax.set_title("Live Festival Buzz: Stage Mentions Over Time", fontsize=14)
    ax.legend(loc="upper left")
    ax.grid(True, linestyle="--", alpha=0.5)

    # Add caption about current buzz peak
    if new_counts:
        peak_stage = max(new_counts, key=new_counts.get)
        peak_val = new_counts[peak_stage]
        ax.text(
            0.95, 0.01,
            f"{peak_stage} just got {peak_val} new mentions",
            transform=ax.transAxes,
            ha="right",
            va="bottom",
            fontsize=10,
            color="darkgreen",
            weight="bold"
        )
    else:
        ax.text(
            0.5, 0.5,
            "Waiting for buzz data...",
            ha="center", va="center"
        )


# Main
if __name__ == "__main__":
    logger.info("Starting EDM Buzzline consumer (line chart)...")
    ani = FuncAnimation(fig, update_chart, interval=2000)  # Update every 2s
    plt.show()
