# buzzline-06-dowdle
P6: Implementing a Custom Streaming Pipeline

# 🎶 EDM Buzzline – Live Festival Buzz Tracker

## Project Overview
EDM Buzzline is a real-time streaming data project that simulates audience buzz during an EDM music festival.  
The system generates messages about artists, stages, and audience reactions, streams them into **Kafka**,  
and then consumes those messages to extract insights and visualize trends with **Matplotlib animation**.  

The goal is to show how streaming data can be used to track *who’s trending, where the energy is, and what the crowd is reacting to* in real time.  

---

## Project Features
- **Producer**:  
  - Generates fake JSON data about festival buzz (artist, stage, reaction, topic, timestamp).  
  - Streams the data into a Kafka topic (`buzzline_edm`).  

- **Consumer**:  
  - Subscribes to the Kafka topic and processes incoming messages.  
  - Tracks trending artists, stages, and audience reactions using dictionaries.  
  - Displays a **live-updating Matplotlib chart** with insights.  

- **Visualization**:    
  - **Line Chart**: Stage mentions over time.  
  - Captions and titles update dynamically (*“DJ Nova leading with 25 mentions”*). 
  - IF there is time: - **Bar Chart**: Top artist mentions in real time. 

---

### 0. If Windows, start WSL
Open a PowerShell terminal in VS Code. Run the following command:
```wsl
```

### 1. Start Kafka
```chmod +x scripts/prepare_kafka.sh
scripts/prepare_kafka.sh
cd ~/kafka
bin/kafka-server-start.sh config/kraft/server.properties
```
**Keep this terminal open!**

In a new WSL terminal, create the topic:
```kafka-topics --create --topic buzzline_edm --bootstrap-server localhost:9092
```

### 2. Run the Producer
In a new powershell terminal
```python producers/edm_producer.py
```

### 3. Run the Consumer
In a new powershell terminal
```python consumers/edm_consumer.py
```

