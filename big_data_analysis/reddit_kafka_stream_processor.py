import json
import logging
from confluent_kafka import Consumer, Producer, KafkaException

class RedditKafkaStreamProcessor:
    """
    Handles Kafka streams
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
        
        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger('confluent_kafka').setLevel(logging.DEBUG)

        self.consumer = Consumer({
            'bootstrap.servers': self.kafka_bootstrap_servers,
            'group.id': 'reddit_consumer_group',
            'auto.offset.reset': 'earliest',
            'debug': 'all', 
        })

        # Initialize producer
        self.producer = Producer(
            {'bootstrap.servers': self.kafka_bootstrap_servers}
        )

        self.consumer.subscribe([self.input_topic])

    def process_messages(self):
        """
        Counts keyword within the stream and sends the count 
        to a specified topic.
        """
        word_counts: dict[str, int] = {}

        try:
            while True:
                msg = self.consumer.poll(timeout=1.0)
                if msg is None:
                    logging.debug("No message received within timeout.")
                    continue
                
                if msg.error():
                    logging.error(f"Consumer error: {msg.error()}")
                    raise KafkaException(msg.error())
                
                logging.debug(f"Received message: {msg.value()}")

                try:
                    message_data = json.loads(msg.value().decode('utf-8'))
                except json.JSONDecodeError as e:
                    logging.error(f"Error decoding JSON: {e}")
                    continue
                
                title = message_data.get("title", "Unknown Title")
                logging.debug(f"Extracted title: {title}")

                if title in word_counts:
                    word_counts[title] += 1
                else:
                    word_counts[title] = 1

                logging.info(f"Processed post: {title}. Count: {word_counts[title]}")

                self.send_to_kafka(title, word_counts[title])

        except KeyboardInterrupt:
            logging.info("Stopped Kafka stream processing")

        except KafkaException as e:
            logging.error(f"KafkaException: {e}")
        
        finally:
            logging.debug("Closing consumer.")
            self.consumer.close()

    def send_to_kafka(
        self, 
        word,
        count
    ):
        """
        Sends data to the "reddit_count" topic.
        """
        message = {
            'word': word,
            'count': count
        }

        try:
            logging.debug(f"Sending message to Kafka: {message}")
            self.producer.produce(self.output_topic, value=json.dumps(message).encode('utf-8'))
            self.producer.flush()
            logging.info(f"Sent to {self.output_topic}: {word} => {count}")

        except Exception as e:
            logging.error(f"Error sending to Kafka: {e}")