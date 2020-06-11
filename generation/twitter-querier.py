import os
import json
import twitter
from typing import List
from urllib.parse import urlencode
from general.leader import LeaderFactory, Leader
from datetime import datetime, timedelta
from tqdm import tqdm


def find_min_id(array: List) -> int:
    return min([item.id for item in array])


def query_leader_for_date(leader: Leader, api: twitter.Api, date: datetime, n_tweets: int = 1000) -> List:
    remaining = n_tweets
    max_id = None
    result = []
    while remaining > 0:
        count = min(remaining, 100)
        remaining -= count
        query_dict = {
            "q": leader.name if leader.search_first_name else leader.name.split()[1] + "-filter:retweets",
            "lang": leader.country.locale.split("-")[0],  # e.g. take "de" from "de-DE"
            "place_country": leader.country.locale.split("-")[1],  # e.g. take "DE" from "de-DE"
            "until": date.strftime("%Y-%m-%d"),
            "since": (date - timedelta(days=1)).strftime("%Y-%m-%d"),
            "count": str(count),
            "tweet_mode": "extended",
            "result_type": "recent",  # one of [recent, popular, mixed]
        }
        if max_id is not None:
            query_dict["max_id"] = str(max_id)

        search_result = api.GetSearch(raw_query=urlencode(query_dict))
        result += search_result

        if len(search_result) != count:
            break

        max_id = find_min_id(search_result)

    return result


def query_leader_yesterday(leader: Leader, api: twitter.Api) -> List:
    return query_leader_for_date(leader, api, datetime.now())


twitter_data = {}
leaders = LeaderFactory().get_leaders(os.path.join("..", "general", "leaders.json"))
api = twitter.Api(consumer_key=os.environ["API_KEY"], consumer_secret=os.environ["API_SECRET"],
                  access_token_key=os.environ["ACCESS_TOKEN"], access_token_secret=os.environ["ACCESS_SECRET"])

for leader in tqdm(leaders):
    twitter_data[leader.name] = [item.full_text for item in query_leader_yesterday(leader, api)]

with open(os.path.join("..", "_data", "raw", datetime.now().strftime("%Y-%m-%d") + ".json"), "w") as out_file:
    json.dump(twitter_data, out_file)
