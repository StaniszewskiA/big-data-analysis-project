import os
import logging
from big_data_analysis import KafkaInfluxConsumer

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    kafka_bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    kafka_topic = os.getenv("KAFKA_TOPIC", "reddit_word_counts")
    
    influx_url = os.getenv("INFLUX_URL", "http://localhost:8086")
    influx_token = os.getenv("INFLUX_TOKEN", "mytoken")
    influx_org = os.getenv("INFLUX_ORG", "myorg")
    influx_bucket = os.getenv("INFLUX_BUCKET", "mybucket")

    # Instantiate our consumer
    consumer = KafkaInfluxConsumer(
        kafka_bootstrap_servers=kafka_bootstrap_servers,
        kafka_topic=kafka_topic,
        influx_url=influx_url,
        influx_token=influx_token,
        influx_org=influx_org,
        influx_bucket=influx_bucket
    )

    consumer.run()