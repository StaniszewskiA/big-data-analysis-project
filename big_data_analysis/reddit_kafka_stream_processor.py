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
        self.consumer = Consumer({
            'bootstrap.servers': self.kafka_bootstrap_servers,
            'group.id': 'reddit_consumer_group',
            'auto.offset.reset': 'earliest'
        })
        self.producer = Producer(
            {'bootstrap.servers': self.kafka_bootstrap_servers}
        )

        self.consumer.subscribe([self.input_topic])

    def process_messages(self):
        """
        Counts keyword occurrences within the stream and sends the count 
        to a specified topic.
        """
        word_counts: dict[str, int] = {}

        try:
            while True:
                msg = self.consumer.poll(timeout=1.0)
                if msg is None:
                    continue
                if msg.error:
                    raise KafkaException(msg.error())
                
                message_data = json.loads(msg.value().decode('utf-8'))
                title = message_data.get("title", "Unknown Title")
                
                words = title.lower().split()  
                
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
        Sends word count data to the "reddit_count" topic.
        """
        try:
            for word, count in word_counts.items():
                message = {
                    'word': word,
                    'count': count
                }
                self.producer.produce(self.output_topic, value=json.dumps(message).encode('utf-8'))
                logging.info(f"Sent to {self.output_topic}: {word} => {count}")
            self.producer.flush()
        except Exception as e:
            logging.error(f"Error sending to Kafka: {e}")
