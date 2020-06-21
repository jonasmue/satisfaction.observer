import os
import json
import twitter

from typing import List
from urllib.parse import urlencode
from category.item import ItemFactory, Item
from datetime import datetime, timedelta
from tqdm import tqdm


class TwitterQuerier:
    def __init__(self, target_file, popular, time_delta, manifest_file):
        self.target_file = target_file
        self.popular = popular
        self.time_delta = time_delta
        self.manifest_file = manifest_file
        self.api = twitter.Api(consumer_key=os.environ["API_KEY"],
                               consumer_secret=os.environ["API_SECRET"],
                               access_token_key=os.environ["ACCESS_TOKEN"],
                               access_token_secret=os.environ["ACCESS_SECRET"])

    @staticmethod
    def find_min_id(array: List) -> int:
        return min([item.id for item in array])

    def query_item_for_date(self, item: Item, n_tweets: int = 1000) -> List:
        """
        Uses a twitter API object to crawl tweets of one day regarding an item

        :param item: The item for which tweets are to be crawled
        :param n_tweets: The number of tweets to be crawled
        :return:
        """
        date = datetime.now() - timedelta(days=self.time_delta)
        remaining = n_tweets
        max_id = None
        result = []
        while remaining > 0:
            count = min(remaining, 100)
            remaining -= count
            query_dict = {
                "q": item.search_term + "-filter:retweets",
                "lang": item.country.locale.split("-")[0],  # e.g. take "de" from "de-DE"
                "until": date.strftime("%Y-%m-%d"),
                "since": (date - timedelta(days=1)).strftime("%Y-%m-%d"),
                "count": str(count),
                "tweet_mode": "extended",
                "result_type": "mixed" if self.popular else "recent",  # one of [recent, popular, mixed]
            }
            if "-" in item.country.locale:
                query_dict["place_country"]: item.country.locale.split("-")[1]  # e.g. take "DE" from "de-DE"

            if max_id is not None:
                query_dict["max_id"] = str(max_id)

            search_result = self.api.GetSearch(raw_query=urlencode(query_dict))
            result += search_result

            if len(search_result) != count:
                break

            max_id = TwitterQuerier.find_min_id(search_result)

        return result

    def run(self):
        twitter_data = {}
        items, _ = ItemFactory().get_items(self.manifest_file)
        print("Querying Twitter for", len(items), "items...")
        for item in tqdm(items):
            twitter_data[item.name] = [{item.id: item.full_text} for item in self.query_item_for_date(item)]
        print("Saving tweets...")
        with open(self.target_file, "w") as out_file:
            json.dump(twitter_data, out_file)
