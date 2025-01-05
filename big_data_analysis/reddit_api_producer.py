import logging
import os
import time
import json
import praw
from kafka import KafkaProducer

class RedditApiWorker():
    def __init__(
        self, 
        call_interval: int, 
        duration: int, 
        reddit_client_id: str, 
        reddit_client_secret: str, 
        reddit_user_agent: str,
        kafka_bootstrap_servers: str,
        kafka_topic: str
    ):
        self.call_interval = call_interval
        self.duration = duration
        self.reddit = praw.Reddit(
            client_id=reddit_client_id,
            client_secret=reddit_client_secret,
            user_agent=reddit_user_agent
        )
        # Kafka Producer
        self.producer = KafkaProducer(
            bootstrap_servers=kafka_bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.kafka_topic = kafka_topic

    def listen(self, subreddit_name: str, method: str = "top", limit: int = 5):
        start_time = time.time()

        while (time.time() - start_time) < self.duration:
            try:
                subreddit = self.reddit.subreddit(subreddit_name)
                fetch_method = getattr(subreddit, method, None)

                if not fetch_method:
                    raise ValueError(f"Invalid method: {method}. Valid methods: 'top', 'new', 'hot'.")

                posts = fetch_method(limit=limit)

                for post in posts:
                    message_data = {
                        "title": post.title,
                        "score": post.score,
                        "url": post.url,
                        "created_utc": post.created_utc,
                        "subreddit": subreddit_name
                    }
                    # Send to Kafka
                    print(message_data)
                    self.producer.send(self.kafka_topic, message_data)

            except Exception as e:
                logging.error(f"Error fetching {method} posts: {e}")

            time.sleep(self.call_interval)

        self.producer.flush()
        print("Finished listening")
