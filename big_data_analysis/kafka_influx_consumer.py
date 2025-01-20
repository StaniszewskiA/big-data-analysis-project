import json
import logging
from kafka import KafkaConsumer
from influxdb_client import InfluxDBClient, Point, WriteOptions

class KafkaInfluxConsumer:
    """
    A consumer that reads messages from a Kafka topic
    and writes them into InfluxDB as time-series data.
    """
    def __init__(
        self,
        kafka_bootstrap_servers: str,
        kafka_topic: str,
        influx_url: str,
        influx_token: str,
        influx_org: str,
        influx_bucket: str
    ):
        self.kafka_bootstrap_servers = kafka_bootstrap_servers
        self.kafka_topic = kafka_topic
        self.influx_url = influx_url
        self.influx_token = influx_token
        self.influx_org = influx_org
        self.influx_bucket = influx_bucket

        self.influx_client = InfluxDBClient(
            url=self.influx_url,
            token=self.influx_token,
            org=self.influx_org
        )

        self.write_api = self.influx_client.write_api(
            write_options=WriteOptions(batch_size=1)
        )

        self.consumer = KafkaConsumer(
            self.kafka_topic,
            bootstrap_servers=self.kafka_bootstrap_servers,
            auto_offset_reset='earliest',
            value_deserializer=lambda m: json.loads(m.decode('utf-8')) if m else None
        )

    def run(self):
        """
        Start consuming messages from Kafka and writing to InfluxDB.
        """
        logging.info(f"Starting KafkaInfluxConsumer on topic: {self.kafka_topic}")
        print(f"Starting consumer for '{self.kafka_topic}' ...")

        for message in self.consumer:
            try:
                # message.key is the word, message.value is the count (assuming your Streams app
                # outputs a key=word, value=count). Adjust parsing if your data structure differs.

                data = message.value
                if not isinstance(data, dict):
                    raise ValueError(f"Expected message.value to be a dictionary, got: {type(data)}")
                
                word = data.get('word', 'unknown')
                count = data.get('count', 0)

                if not isinstance(count, (int, float)):
                    raise TypeError(f"Unsupported type for 'count': {type(count)}")

                point = Point("reddit_word_counts") \
                    .tag("word", word) \
                    .field("count", count) \
                    .time(None)

                self.write_api.write(bucket=self.influx_bucket, record=point)
                logging.info(f"Wrote to InfluxDB: {word} => {count}")
                print(f"Wrote to InfluxDB: {word} => {count}")

            except Exception as e:
                logging.error(f"Error processing message: {e}")
                print(f"Error processing message: {e}")
