import json

from category.item import ItemFactory


class TextCleaner:

    def __init__(self, source_file, target_file, manifest_file):
        self.source_file = source_file
        self.target_file = target_file
        self.manifest_file = manifest_file

    @staticmethod
    def should_ignore_word(item, word):
        split = item.name.lower().split()
        if len(split) > 1:
            for split_part in split[:-1]:
                if split_part in word:
                    return True
        return word.startswith("@") or "http" in word

    @staticmethod
    def clean_word(item, word, replacement_dict):
        last_part = item.name.lower().split()[-1]
        if word.startswith("#"):
            word = word[1:]
        if last_part in word:
            word = replacement_dict[item.country.locale.split("-")[0]]
        return word

    @staticmethod
    def clean_tweet(item, tweet, replacement_dict):
        tweet_tokens = []
        for word in list(tweet.values())[0].split():
            word = word.lower()
            if TextCleaner.should_ignore_word(item, word):
                continue
            else:
                tweet_tokens.append(TextCleaner.clean_word(item, word, replacement_dict))

        return " ".join(tweet_tokens)

    @staticmethod
    def clean_tweets(item, tweets, replacement_dict):
        return [TextCleaner.clean_tweet(item, tweet, replacement_dict) for tweet in tweets]

    def run(self):
        with open(self.source_file, "r") as input_file:
            tweets_by_item = json.load(input_file)
        items, replacement_dict = ItemFactory().get_items(self.manifest_file)
        cleaned_by_item = {}

        for item_name, tweets in tweets_by_item.items():
            item = [item for item in items if item.name == item_name][0]
            cleaned_by_item[item.name] = TextCleaner.clean_tweets(item, tweets, replacement_dict)

        with open(self.target_file, "w") as output_file:
            json.dump(cleaned_by_item, output_file)
