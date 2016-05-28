#!/usr/bin/env python3

"""Collect tweets from Twitter"""

import json
import time

import tweepy

import secrets

auth = tweepy.OAuthHandler(secrets.CONSUMER_KEY, secrets.CONSUMER_SECRET)
auth.set_access_token(secrets.ACCESS_TOKEN, secrets.ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

TWEETS = []
MAX_TWEETS = 1000

def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            time.sleep(15 * 60)

for i, tweet in enumerate(limit_handled(tweepy.Cursor(api.list_timeline, "FettAPI", "trucks").items())):
    print("Getting tweet {}".format(i))
    TWEETS.append(tweet)
    if len(TWEETS) >= MAX_TWEETS:
        break

if TWEETS:
    with open("tweets.json", "w") as outfile:
        json.dump([tweet._json for tweet in TWEETS], outfile)
