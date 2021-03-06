import json

from tqdm import tqdm
from transformers import *


class SemanticClassificationAnalyzer:
    def __init__(self, source_file, target_file):
        self.source_file = source_file
        self.target_file = target_file
        self.tokenizer = AutoTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
        self.model = AutoModelForSequenceClassification.from_pretrained(
            "nlptown/bert-base-multilingual-uncased-sentiment")
        self.sentiment_analyzer = TextClassificationPipeline(model=self.model, tokenizer=self.tokenizer)

    def run(self):
        with open(self.source_file, "r") as input_file:
            tweets = json.load(input_file)

        print("Predicting classes for", len(tweets), "items ...")
        classification = {}
        for item, item_tweets in tweets.items():
            print("\nPredicting classes for", item, "...")
            classification[item] = []
            for tweet in tqdm(item_tweets):
                c = self.sentiment_analyzer(tweet)[0]
                classification[item].append((int(c["label"].split()[0]), c["score"]))
        with open(self.target_file, "w") as output_file:
            json.dump(classification, output_file)
