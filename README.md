# Big data pipeline project

This repository demonstrates a **big data pipeline** that fetches data from the **Reddit API**, uses **Kafka Streams** to analyze word frequency, stores results in **InfluxDB**, and visualizes them in **Grafana**.

## Table of Contents
- [Big data pipeline project](#big-data-pipeline-project)
  - [Table of Contents](#table-of-contents)
  - [1. Overview](#1-overview)
  - [2. Prerequisites](#2-prerequisites)
  - [3. Quick Start](#3-quick-start)
    - [3.1. Clone the Repository](#31-clone-the-repository)
    - [3.2. Set Up Python Environment](#32-set-up-python-environment)
      - [1. (Optional) Create a Python Virtual Environment](#1-optional-create-a-python-virtual-environment)
      - [2. Install Python Dependencies](#2-install-python-dependencies)
    - [3.3. Infrastructure via Docker Compose](#33-infrastructure-via-docker-compose)
    - [3.4. Creating Kafka Topics](#34-creating-kafka-topics)
    - [3.5. Running the Python Producer](#35-running-the-python-producer)
    - [3.6. Manual Kafka Testing](#36-manual-kafka-testing)
    - [3.7. Running the Python Consumer](#37-running-the-python-consumer)
    - [3.8. Access InfluxDB](#38-access-influxdb)
    - [3.9. Access Grafana](#39-access-grafana)
  - [4 Future Improvements](#4-future-improvements)

---

## 1. Overview

This project focuses on **real-time data ingestion and analysis** using:

- **Reddit API** to fetch live posts and comments.
- **Apache Kafka** for streaming data ingestion.
- **Kafka Streams** (Scala/Java) to process and compute word frequencies (currently work-in-progress).
- **InfluxDB** as a time-series database to store aggregated metrics (word counts, etc.).
- **Grafana** to visualize the trends and results in real time.

The pipeline is designed to **collect** data from Reddit, **transform** or **analyze** it (e.g., by counting word frequencies), and **store** it in InfluxDB for easy visualization in Grafana.

---

## 2. Prerequisites

- **Docker** and **Docker Compose** installed on your system.
- **Python 3.7+** (to run the producer and consumer scripts).
- A **Git** client to clone this repository (optional; you may download the code as a ZIP, too).

---

## 3. Quick Start

### 3.1. Clone the Repository

```bash
git clone https://github.com/your-username/big-data-analysis-project.git
cd big-data-analysis-project
```
### 3.2. Set Up Python Environment
#### 1. (Optional) Create a Python Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Or venv\Scripts\activate on Windows
```
#### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```
Ensure **requirements.txt** includes libraries such as:
- praw (for Reddit API)
- kafka-python
- influxdb-client


### 3.3. Infrastructure via Docker Compose
You can set the infrastructure up by running:
```bash
docker-compose up -d
```
This starts:

- Zookeeper (manages Kafka cluster metadata)
- Kafka (event streaming platform)
- InfluxDB (time-series database)
- Grafana (dashboard visualization)

Wait a few seconds for all services to initialize. Use docker-compose logs -f if you need to see container logs.

### 3.4. Creating Kafka Topics
If you need specific topics for your pipeline, you can create them by logging into the Kafka container:

```bash
docker exec -it kafka bash

# Inside the container, create topics:

kafka-topics.sh --create \
  --topic reddit_posts \
  --bootstrap-server localhost:9092 \
  --partitions 1 --replication-factor 1

kafka-topics.sh --create \
  --topic reddit_word_counts \
  --bootstrap-server localhost:9092 \
  --partitions 1 --replication-factor 1
```
### 3.5. Running the Python Producer
If you have a Reddit Producer script (e.g., producer_script.py) that fetches data from the Reddit API and sends it to Kafka, run:

```bash
python producer_script.py
```
It will:

- Fetch Reddit posts via praw.
- Publish them to the reddit_posts Kafka topic.
- (Make sure you’ve set your Reddit credentials either as environment variables or in the code.)

### 3.6. Manual Kafka Testing
Send and Read messages in Kafka without scripts—use the console producer/consumer.

Produce test messages:

```bash
docker exec -it kafka bash

kafka-console-producer.sh \
  --broker-list localhost:9092 \
  --topic reddit_word_counts \
  --property "parse.key=true" \
  --property "key.separator=:"
```
Type some messages. (i.e. python:10) press Enter after each. Ctrl+C to exit.

Consume messages:
```bash
docker exec -it kafka bash
kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic reddit_posts \
  --from-beginning
```
This will print all messages in the topic from the earliest offset.

### 3.7. Running the Python Consumer
A consumer script (e.g., consumer_script.py) can read data (like word counts) from Kafka and store it in InfluxDB:

```bash
python consumer_script.py
```
Make sure you have the correct token for InfluxDB 2.x; simply using username/password is not enough.

By default, you might read from reddit_word_counts and store data under the measurement reddit_word_counts in InfluxDB.

### 3.8. Access InfluxDB
- InfluxDB is available at http://localhost:8086.
- Log in with credentials from docker-compose.yml (e.g., admin / admin123 if that was set).
- You can create or retrieve a token in the UI.
- 
Your data is stored in the bucket you defined (e.g., mybucket).

### 3.9. Access Grafana
Grafana runs on port 3000. So visit:

```bash
http://localhost:3000
```

- Default user: admin
- Default pass: admin123 (as set in the compose file)

Add a Data Source:

- Go to Configuration → Data Sources → Add data source.
- Select InfluxDB.
- Enter URL as http://influxdb:8086 (if referencing by container name) or http://localhost:8086 if from your host.
- Use the organization (e.g., myorg) and the token you created/found in InfluxDB.
- Once configured, you can create dashboards and panels to visualize the data streaming in.

## 4 Future Improvements

Implement Kafka Streams: Create a Scala/Java application to read from reddit_posts and write aggregated word counts (or other analyses) to reddit_word_counts.

Add NLP: Enhance the pipeline with sentiment analysis or entity extraction.
Automate Producer/Consumer: 

Containerize producer/consumer scripts so they run automatically rather than by hand.

Security: For production, enable SSL/TLS for Kafka, secure tokens in a secrets manager, etc.
