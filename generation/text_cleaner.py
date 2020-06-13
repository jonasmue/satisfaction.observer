import os
import json
from datetime import datetime, timedelta
from general.leader import LeaderFactory

DATA_DIR = os.path.join("..", "_data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
CLEANED_DIR = os.path.join(DATA_DIR, "cleaned")

POPULAR = False
TIME_DELTA_DAYS = 7

date = (datetime.now() - timedelta(days=TIME_DELTA_DAYS)).strftime("%Y-%m-%d")
popular_suffix = "_popular" if POPULAR else ""

leader_term_for_lang = {
    "en": "president",
    "de": "präsident",
    "fr": "président",
    "nl": "president",
    "it": "presidente",
    "es": "presidente"
}

def should_ignore_word(leader, word):
    return leader.name.split()[0] in word or word.startswith("@") or "http" in word


def clean_word(leader, word):
    last_name = leader.name.split()[1]
    if word.startswith("#"):
        word = word[1:]
    if last_name in word:
        word = leader_term_for_lang[leader.country.locale.split("-")[0]]
    word = word.lower()
    return word


def clean_tweet(leader, tweet):
    tweet_tokens = []
    for word in tweet.split():
        if should_ignore_word(leader, word):
            continue
        else:
            tweet_tokens.append(clean_word(leader, word))

    return " ".join(tweet_tokens)


def clean_tweets(leader, tweets):
    return [clean_tweet(leader, tweet) for tweet in tweets]


file_name = date + popular_suffix + ".json"
with open(os.path.join(RAW_DIR, file_name), "r") as input_file:
    tweets_by_leader = json.load(input_file)

cleaned_by_leader = {}

leaders = LeaderFactory().get_leaders(os.path.join("..", "general", "leaders.json"))

for leader_name, tweets in tweets_by_leader.items():
    leader = [leader for leader in leaders if leader.name == leader_name][0]
    cleaned_by_leader[leader.name] = clean_tweets(leader, tweets)

with open(os.path.join(CLEANED_DIR, file_name), "w") as output_file:
    json.dump(cleaned_by_leader, output_file)
