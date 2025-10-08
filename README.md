# buzzline-06-dowdle
P6: Implementing a Custom Streaming Pipeline

# 🎶 EDM Buzzline (Live Festival Buzz Tracker)

## Project Overview
EDM Buzzline is a real-time streaming data project that simulates audience buzz during an EDM festival.  
The pipeline uses a producer to generate messages, streams them into **Kafka**, and then uses a consumer to process the messages and extract insights and visualize trends with **Matplotlib animation**.  

The goal is to show how streaming data can be used to track *who’s trending, where the energy is, and what the crowd is most excited about* in real time.  

---

## Project Features
- **Producer**:  
  - Generates synthetic JSON data about festival buzz (artist, stage, reaction, topic, timestamp).  
  - Streams the data into a Kafka topic (`buzzline_edm`).

Each message from the producer is a JSON object, for example:

```json
{
  "artist": "Excision",
  "stage": "Prehistoric Stage",
  "reaction": "🦖",
  "timestamp": "2025-10-02T20:30:15"
}
```  

- **Consumer**:  
  - Subscribes to the Kafka topic and processes incoming messages. 
  - Logs the message by appending to `edm_live.json` 
  - Tracks trending artists, stages, and audience reactions using dictionaries.  
  - Displays a **live-updating Matplotlib chart** with insights.  

- **Visualization**:  
  - **Bar Chart**: Top artist mentions in real time. 
  - **Line Chart**: Stage mentions over time.  
  - Captions and titles update dynamically (*“Excision leading with 25 mentions”*).  

---

### 0. If Windows, start WSL
Open a PowerShell terminal in VS Code. Run the following command:
```
wsl
```

### 1. Start Kafka
```
cd ~/kafka

# Generate cluster UUID
KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"
echo "Generated Cluster ID: $KAFKA_CLUSTER_ID"

# Format storage with the cluster ID
bin/kafka-storage.sh format -t $KAFKA_CLUSTER_ID -c config/kraft/server.properties

# Verify configuration file exists
ls -la config/kraft/server.properties

# start kafka broker
bin/kafka-server-start.sh config/kraft/server.properties
```
**Keep this terminal open!**

In a new WSL terminal, create the topic:
```
WSL
cd ~/kafka
kafka-topics --create --topic buzzline_edm --bootstrap-server localhost:9092
```

Verify topic was successfully created
```
bin/kafka-topics.sh --list --bootstrap-server localhost:9092
```

### 2. Run the Producer
In a new powershell terminal
```
python -m producers.edm_producer
```

### 3. Run the Consumer
In a another new powershell terminal
``` 
# Bar Chart Consumer
python -m consumers.edm_consumer
```
``` 
# Line Chart Consumer
python -m consumers.edm_consumer_line
```

You should see a live animated chart updating as new buzz messages stream in.

****

## Dynamic Visualization
1. Bar Chart (Artist Mentions)
  Updated every 3 seconds, it provides a snapshot of which artists are drawing the most attention:
  * X-axis: Artists
  * Y-axis: Total Mentions
  * Caption: Highlights which artist is currently the most popular
Example Screenshots:
![Artist Bar Chart]("C:\Users/Britt/Documents/44671/Screenshot 2025-10-07 181453.png")
1. Line Chart (Stage Mentions Over Time)
  Updated every 3 seconds, it visualizes audience trends across stages as the festival progresses: 
  * X-axis: Time (update intervals)
  * Y-axis: Mentions per interval
  * Lines: One per stage
  * Caption: Highlights which stage currently has the biggest crowd
Example Screenshots:
![Stage Line Chart]("C:/Users/Britt/Documents/44671/Screenshot 2025-10-07 181637.png")

****
## Insight
This project demonstrates how streaming pipelines can provide real-time crowd analytics for festivals. In a real deployment, similar pipelines could:

- Track social media buzz for artists in real-time

- Alert organizers when a stage is becoming overcrowded

- Optimize scheduling or promotions based on live feedback

Thank you for taking the time to review my project!
