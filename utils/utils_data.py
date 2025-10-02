# Predefined lists of artists, stages, reactions, and topics
# for the EDM Buzzline producer.
import random
from datetime import datetime

# List of artists (can expand as needed)
ARTISTS = [
    "Excision",
    "Gorilla T",
    "Adventure Club",
    "Skrillex",
    "Subtronics",
    "Zeds Dead",
    "Slander",
    "Rezz",
    "Galantis",
    "DrinkUrWater"
]

# List of stages
STAGES = [
    "Prehistoric Stage",
    "Wompy Woods",
    "Forest Stage",
    "Raptor Valley",
    "The Crater"
]

# List of audience reactions (emojis or words)
REACTIONS = [
    "🔥", "🦖", "🕺", "🎉", "🤖", "🦣", "🌋", "😍", "❌", "🫠"
]

# List of buzz topics
TOPICS = [
    "drones",
    "bass face",
    "side quest",
    "pyro",
    "lasers",
    "B2B",
    "detox",
    "rail ride",
    "special guest"
]


def generate_message() -> dict:
    """
    Generate a random EDM buzzline message with current timestamp.
    
    Returns:
        dict: A message containing festival buzz info.
    """
    return {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "stage": random.choice(STAGES),
        "artist": random.choice(ARTISTS),
        "reaction": random.choice(REACTIONS),
        "topic": random.choice(TOPICS)
    }


# Example usage for testing
if __name__ == "__main__":
    for _ in range(3):
        print(generate_message())