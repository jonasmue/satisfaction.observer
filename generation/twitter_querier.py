import os
import json
import twitter

from typing import List
from urllib.parse import urlencode
from general.leader import LeaderFactory, Leader
from datetime import datetime, timedelta
from tqdm import tqdm


class TwitterQuerier:
    def __init__(self, target_file, popular, time_delta, leaders_file):
        self.target_file = target_file
        self.popular = popular
        self.time_delta = time_delta
        self.leaders_file = leaders_file
        self.api = twitter.Api(consumer_key=os.environ["API_KEY"],
                               consumer_secret=os.environ["API_SECRET"],
                               access_token_key=os.environ["ACCESS_TOKEN"],
                               access_token_secret=os.environ["ACCESS_SECRET"])

    @staticmethod
    def find_min_id(array: List) -> int:
        return min([item.id for item in array])

    def query_leader_for_date(self, leader: Leader, n_tweets: int = 1000) -> List:
        """
        Uses a twitter API object to crawl tweets of one day regarding a leader

        :param leader: The leader for whom tweets are to be crawled
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
                "q": (leader.name if leader.search_first_name else leader.name.split()[1]) + "-filter:retweets",
                "lang": leader.country.locale.split("-")[0],  # e.g. take "de" from "de-DE"
                "place_country": leader.country.locale.split("-")[1],  # e.g. take "DE" from "de-DE"
                "until": date.strftime("%Y-%m-%d"),
                "since": (date - timedelta(days=1)).strftime("%Y-%m-%d"),
                "count": str(count),
                "tweet_mode": "extended",
                "result_type": "mixed" if self.popular else "recent",  # one of [recent, popular, mixed]
            }
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
        leaders = LeaderFactory().get_leaders(self.leaders_file)
        print("Querying Twitter for", len(leaders), "leaders...")
        for leader in tqdm(leaders):
            twitter_data[leader.name] = [{item.id: item.full_text} for item in self.query_leader_for_date(leader)]
        print("Saving tweets...")
        with open(self.target_file, "w") as out_file:
            json.dump(twitter_data, out_file)
