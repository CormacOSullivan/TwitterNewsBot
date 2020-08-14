#!/usr/bin/env python

import logging
import sys
import time
import os

import TweepyAPI
import GoogleNewsScraper

KEYWORDS = ["location:"]


def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()

    current_path = os.path.abspath(os.path.dirname(__file__))
    tweet_file_path = os.path.join(current_path, "Addons", "tweet_id.txt")
    json_file_path = os.path.join(current_path, "Addons", "countries.json")

    extra_params = {"tbm": "nws"}
    article_num = 3

    # Read in keys and tokens set as environmental variables
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    tweepyAPI = TweepyAPI.TweepyAPI(consumer_key, consumer_secret, access_token, access_token_secret, logger,
                                    tweet_file_path)
    googleAPI = GoogleNewsScraper.GoogleNewsScraper(json_file_path, logger)

    countries_data = googleAPI.read_json()
    since_id = tweepyAPI.read_tweet_id()
    old_id = since_id
    # Check for any incorrect initialisations of required variables
    if any(x == -1 for x in [tweepyAPI.api, countries_data, since_id] or any(
            y is None for y in [consumer_key, consumer_secret, access_token_secret])):
        logger.error("An error has occurred during the setup of the system: Please check the logs for more information")
        sys.exit()
    while True:
        try:
            location_name, since_id = tweepyAPI.check_mentions(KEYWORDS, since_id, countries_data)
            if location_name:
                links, titles = googleAPI.get_search_results(location_name, article_num, extra_params)
                tweet_string = googleAPI.create_tweet(location_name, links, titles)
                tweepyAPI.reply_to_tweet(tweet_string, since_id)
            if since_id > old_id:
                tweepyAPI.save_tweet_id(since_id)
                old_id = since_id
            logger.info("Waiting...")
            time.sleep(20)
        except KeyboardInterrupt:
            sys.exit()


if __name__ == "__main__":
    main()
