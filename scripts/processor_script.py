import logging
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from big_data_analysis import RedditKafkaStreamProcessor

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    kafka_bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    input_topic = os.getenv("KAFKA_INPUT_TOPIC", "reddit_posts")
    output_topic = os.getenv("KAFKA_OUTPUT_TOPIC", "reddit_count")

    stream_processor = RedditKafkaStreamProcessor(
        kafka_bootstrap_servers=kafka_bootstrap_servers,
        input_topic=input_topic,
        output_topic=output_topic
    )

    stream_processor.process_messages()
