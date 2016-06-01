"""Collects statuses from Twitter"""

import json
import logging
import time
from typing import Any, Dict, Iterable

import tweepy

from fett import secrets

logger = logging.getLogger("fett.twitter")

def limit_handled(cursor: tweepy.Cursor):
    """Wrap cursor access with rate limiting

    :param cursor: The cursor to siphon
    :returns: Cursor items

    """
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            time.sleep(15 * 60)

class TwitterCollector:
    """Now it's time for things I found in Tweets"""

    def __init__(self, account_name: str, source_list: str) -> None:
        """Init!"""
        self._auth = tweepy.OAuthHandler(secrets.CONSUMER_KEY, secrets.CONSUMER_SECRET)
        self._auth.set_access_token(secrets.ACCESS_TOKEN, secrets.ACCESS_TOKEN_SECRET)
        self._api = tweepy.API(self._auth)
        self.account_name = account_name
        self.source_list = source_list

    def collect(self, since_id: str=None) -> Iterable[Dict[str, Any]]:
        """Collect tweets

        :param since_id: TODO
        :returns: TODO

        """
        logger.debug("Collecting tweets")
        data = json.load(open("tweets-5.json", "r"))
        yield from data
        # for page in limit_handled(tweepy.Cursor(self._api.list_timeline, self.account_name,
        #                                         self.source_list).pages(1)):
        #     yield from page
