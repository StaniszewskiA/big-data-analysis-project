import pytest
import praw
import time

from big_data_analysis.reddit_api_worker import RedditApiWorker

"""
Nie mam pojęcia jak mockować praw.Reddit, trzeba ale się ten przyjrzeć, 
albo w ogóle nie testować i liczyć, że wszystko będzie śmigać.
"""

@pytest.fixture
def reddit_api_worker(mocker):
    mock_reddit = mocker.patch('praw.Reddit', autospec=True)
    mock_subreddit = mocker.Mock()

    mock_subreddit.top.return_value = [
        {"title": "Post 1", "score": 100, "url": "http://post1.com"},
        {"title": "Post 2", "score": 200, "url": "http://post2.com"}
    ]

    mock_reddit.return_value.subreddit.return_value = mock_subreddit
    

    return RedditApiWorker(
        call_interval=1,
        duration=5,
        reddit_client_id="fake_client_id",
        reddit_client_secret="fake_client_secret",
        reddit_user_agent="fake_user_agent"
    )

def test_listen_fetches_top_posts(reddit_api_worker):
    result = reddit_api_worker.listen("python", "top", limit=2)

    assert len(result) == 1 # Zdążymy zwrócić jeden batch z wynikami...
    assert len(result[2]) == 2 # ... w którym będą dwa posty