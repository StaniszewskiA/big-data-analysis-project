import logging
import os
import time

import praw

class RedditApiWorker():
    def __init__(
        self, 
        call_interval: int, 
        duration: int, 
        reddit_client_id: str, 
        reddit_client_secret: str, 
        reddit_user_agent: str
    ):
        self.call_interval = call_interval
        self.duration = duration
        self.reddit = praw.Reddit(
            client_id=reddit_client_id,
            client_secret=reddit_client_secret,
            user_agent=reddit_user_agent
        )

    def listen(self, subreddit_name: str, method: str = "top", limit: int = 5):
        result = []
        start_time = time.time()

        while (time.time() - start_time) < self.duration:
            try:
                subreddit = self.reddit.subreddit(subreddit_name)
                fetch_method = getattr(subreddit, method, None)

                # TODO: Upewnić się dla jakich metod klasa nie rzuci tego błędu
                if not fetch_method:
                    raise ValueError(f"Invalid method: {method}. Valid method are 'top', 'new', or 'hot'.")
                
                posts = fetch_method(limit=limit)
                result.append([
                    {"title": post.title, "score": post.score, "url": post.url}
                    for post in posts
                ])

            except Exception as e:
                print(f"Error fetching {method} posts: {e}")

            time.sleep(self.call_interval)

        print("Finished listening")
        return result
    
    def send_to_kafka():
        # TODO
        pass


# if __name__ == "__main__":
#     logging.basicConfig(level=logging.DEBUG)

#     raw = RedditApiWorker(
#         call_interval=10, 
#         duration=30, 
#         reddit_client_id=os.getenv("REDDIT_CLIENT_ID"),
#         reddit_client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
#         reddit_user_agent=os.getenv("REDDIT_USER_AGENT")
#     )

#     results = raw.listen("python", "new")

#     print(results)