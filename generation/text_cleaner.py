import json
import os

from general.leader import LeaderFactory


class TextCleaner:
    leader_term_for_lang = {
        "en": "president",
        "de": "präsident",
        "fr": "président",
        "nl": "president",
        "it": "presidente",
        "es": "presidente"
    }

    def __init__(self, source_file, target_file, leaders_file):
        self.source_file = source_file
        self.target_file = target_file
        self.leaders_file = leaders_file

    @staticmethod
    def should_ignore_word(leader, word):
        return leader.name.split()[0] in word or word.startswith("@") or "http" in word

    @staticmethod
    def clean_word(leader, word):
        last_name = leader.name.split()[1]
        if word.startswith("#"):
            word = word[1:]
        if last_name in word:
            word = TextCleaner.leader_term_for_lang[leader.country.locale.split("-")[0]]
        word = word.lower()
        return word

    @staticmethod
    def clean_tweet(leader, tweet):
        tweet_tokens = []
        for word in list(tweet.values())[0].split():
            if TextCleaner.should_ignore_word(leader, word):
                continue
            else:
                tweet_tokens.append(TextCleaner.clean_word(leader, word))

        return " ".join(tweet_tokens)

    @staticmethod
    def clean_tweets(leader, tweets):
        return [TextCleaner.clean_tweet(leader, tweet) for tweet in tweets]

    def run(self):
        with open(self.source_file, "r") as input_file:
            tweets_by_leader = json.load(input_file)
        leaders = LeaderFactory().get_leaders(self.leaders_file)
        cleaned_by_leader = {}

        for leader_name, tweets in tweets_by_leader.items():
            leader = [leader for leader in leaders if leader.name == leader_name][0]
            cleaned_by_leader[leader.name] = TextCleaner.clean_tweets(leader, tweets)

        with open(self.target_file, "w") as output_file:
            json.dump(cleaned_by_leader, output_file)
