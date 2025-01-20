import argparse
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from big_data_analysis import RedditApiWorker

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reddit Scraper")
    parser.add_argument("subreddit", type=str, help="The subreddit to listen to")
    args = parser.parse_args()

    reddit_client_id = os.getenv("REDDIT_CLIENT_ID", "your_client_id")
    reddit_client_secret = os.getenv("REDDIT_CLIENT_SECRET", "your_client_secret")
    reddit_user_agent = os.getenv("REDDIT_USER_AGENT", "my_reddit_scraper")

    kafka_bootstrap_servers = "localhost:9092"
    kafka_topic = "reddit_posts"

    raw = RedditApiWorker(
        call_interval=30, 
        duration=3600, 
        reddit_client_id=reddit_client_id,
        reddit_client_secret=reddit_client_secret,
        reddit_user_agent=reddit_user_agent,
        kafka_bootstrap_servers=kafka_bootstrap_servers,
        kafka_topic=kafka_topic
    )

    raw.listen(args.subreddit, "new", limit=5)
