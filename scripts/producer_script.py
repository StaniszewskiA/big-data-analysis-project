import os
from big_data_analysis import RedditApiWorker

if __name__ == "__main__":
    reddit_client_id = os.getenv("REDDIT_CLIENT_ID", "your_client_id")
    reddit_client_secret = os.getenv("REDDIT_CLIENT_SECRET", "your_client_secret")
    reddit_user_agent = os.getenv("REDDIT_USER_AGENT", "my_reddit_scraper")

    kafka_bootstrap_servers = "localhost:9092"
    kafka_topic = "reddit_posts"

    raw = RedditApiWorker(
        call_interval=5, 
        duration=30, 
        reddit_client_id=reddit_client_id,
        reddit_client_secret=reddit_client_secret,
        reddit_user_agent=reddit_user_agent,
        kafka_bootstrap_servers=kafka_bootstrap_servers,
        kafka_topic=kafka_topic
    )

    raw.listen("Python", "new", limit=5)
