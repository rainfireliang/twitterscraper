from datetime import datetime

from bs4 import BeautifulSoup
from coala_utils.decorators import generate_ordering


@generate_ordering('timestamp', 'id', 'rtid','text', 'user')
class Tweet:
    def __init__(self, user, id, rtid,timestamp, fullname, text):
        self.user = user
        self.id = id
        self.rtid = rtid
        self.timestamp = timestamp
        self.fullname = fullname
        self.text = text

    @classmethod
    def from_soup(cls, tweet):
        return cls(
            user=tweet.find('span', 'username').text[1:],
            id=tweet['data-item-id'],
            rtid=tweet.find('div','tweet')['data-retweet-id'],
            timestamp=datetime.utcfromtimestamp(
                int(tweet.find('span', '_timestamp')['data-time'])),
            fullname=tweet.find('strong', 'fullname').text,
            text=tweet.find('p', 'tweet-text').text
            if tweet.find('p', 'tweet-text') else ""
        )

    @classmethod
    def from_html(cls, html):
        soup = BeautifulSoup(html, "lxml")
        tweets = soup.find_all('li', 'js-stream-item')
        if tweets:
            for tweet in tweets:
                try:
                    yield cls.from_soup(tweet)
                except AttributeError:
                    pass  # Incomplete info? Discard!
