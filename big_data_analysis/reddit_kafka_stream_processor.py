import json
import logging

from kafka import KafkaConsumer, KafkaProducer

class RedditKafkaStreamProcessor:
    """
    Handles Kafka streams.
    """
    def __init__(
        self,
        kafka_bootstrap_servers: str, 
        input_topic: str, 
        output_topic: str
    ):
        self.kafka_bootstrap_servers = kafka_bootstrap_servers
        self.input_topic = input_topic
        self.output_topic = output_topic

        self.consumer = KafkaConsumer(
            self.input_topic,
            bootstrap_servers=self.kafka_bootstrap_servers,
            group_id='reddit_consumer_group',
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )

        self.producer = KafkaProducer(
            bootstrap_servers=self.kafka_bootstrap_servers,
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )

    def process_messages(self):
        """
        Counts keyword occurrences within the stream and sends the count 
        to a specified topic.
        """
        word_counts: dict[str, int] = {}

        try:
            logging.info(f"Starting to process messages from topic '{self.input_topic}'...")
            for message in self.consumer:
                message_data = message.value
                title = message_data.get("title", "Unknown Title")
                
                words = [word.strip() for word in title.lower().split()]
                
                for word in words:
                    if word in word_counts:
                        word_counts[word] += 1
                    else:
                        word_counts[word] = 1

                logging.info(f"Processed post: {title}. Current word counts: {word_counts}")

                self.send_to_kafka(word_counts)
                
        except KeyboardInterrupt:
            logging.info("Stopped Kafka stream processing")
        finally:
            self.consumer.close()

    def send_to_kafka(self, word_counts: dict):
        """
        Sends word count data to the output topic.
        """
        try:
            for word, count in word_counts.items():
                message = {
                    'word': word,
                    'count': count
                }
                self.producer.send(self.output_topic, value=message)
                logging.info(f"Sent to {self.output_topic}: {word} => {count}")
            self.producer.flush()
        except Exception as e:
            logging.error(f"Error sending to Kafka: {e}")