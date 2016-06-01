#!/usr/bin/env python3
"""The Fett daemon"""

import argparse
import asyncio
import logging
import sys
import time
from typing import Dict, Any

from fett.twitter_collector import TwitterCollector

logging.basicConfig(stream=sys.stderr)

logger = logging.getLogger("fett.daemon")

TWEET_QUEUE = asyncio.Queue()

def extract(tweet: Dict[str, Any]) -> str:
    """Extract a tweet

    :param tweet: The tweet to extract
    :returns: The tweet ID

    """
    logging.debug("Extracting: %s", tweet["id"])
    time.sleep(5)
    return tweet["id"]

async def enrich() -> None:
    """Basic enrichment tick"""
    while True:
        tweet = await TWEET_QUEUE.get()
        logger.info("[%s] -> Processing", tweet["id"])
        final = extract(tweet)
        logger.debug("[%s] <- Processing done: %s", tweet["id"], final)
        await asyncio.sleep(1)

async def collect(twitter_collector, interval) -> None:
    """Collect the tweets"""
    while True:
        for tweet in twitter_collector.collect():
            logger.info("[%s] Collected", tweet["id"])
            TWEET_QUEUE.put_nowait(tweet)
        await asyncio.sleep(interval)

def start_collection(interval: int, since_id: str=None) -> None:
    """Start the collection loop.

    This runs indefinitely.

    :param interval: The interval (in seconds) with which to run the collector
    :param loop: The AsyncIO event loop onto which enrichment tasks should be    pushed
    :param since_id: An optional ID to start collection after

    """
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    twitter_collector = TwitterCollector("FettAPI", "trucks")
    loop.create_task(collect(twitter_collector, interval))
    loop.create_task(enrich())
    try:
        loop.run_forever()
    finally:
        loop.close()

def main():
    """The main event loop

    :returns: TODO

    """
    args = parse_args()
    logging.getLogger("fett").setLevel(logging.DEBUG if args.verbose else logging.INFO)
    start_collection(args.interval)

def parse_args():
    """Parse the command line args
    :returns: TODO

    """
    parser = argparse.ArgumentParser(description="The Fett daemon",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", "--interval", dest="interval", type=int, default=3,
                        help="The interval (in minutes)")
    parser.add_argument("-v", dest="verbose", action="store_true")
    return parser.parse_args()

if __name__ == "__main__":
    main()
