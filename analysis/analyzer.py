import os
import json
from transformers import *
from tqdm import tqdm
from datetime import datetime, timedelta
from time import time

TIME_DELTA_DAYS = 0
POPULAR = False

for TIME_DELTA_DAYS in range(6, 8):
    DATE = (datetime.now() - timedelta(days=TIME_DELTA_DAYS)).strftime("%Y-%m-%d")

    DATA_DIR = os.path.join("..", "_data")
    ANALYZED_DATA_DIR = os.path.join(DATA_DIR, "analyzed")

    popular_suffix = "_popular" if POPULAR else ""
    RAW_FILE = os.path.join(DATA_DIR, "cleaned", DATE + popular_suffix + ".json")
    CLASSIFICATION_FILE = os.path.join(ANALYZED_DATA_DIR, DATE + popular_suffix + "_classifications.json")
    OUTPUT_FILE = os.path.join(ANALYZED_DATA_DIR, DATE + popular_suffix + "_classifications-mean-normalized.json")

    tokenizer = AutoTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
    model = AutoModelForSequenceClassification.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
    sentiment_analyzer = TextClassificationPipeline(model=model, tokenizer=tokenizer)

    print("Opening", RAW_FILE)
    with open(RAW_FILE, "r") as input_file:
        tweets = json.load(input_file)

    print("Predicting classes for", len(tweets), "leaders ...")
    classification = {}
    start = time()
    for leader, leader_tweets in tweets.items():
        print("Predicting classes for", leader, "...")
        classification[leader] = []
        for tweet in tqdm(leader_tweets):
            c = sentiment_analyzer(tweet)[0]
            classification[leader].append((int(c["label"].split()[0]), c["score"]))
    print("Done. Took {} seconds".format(time() - start))

    print("Saving classes...")
    with open(CLASSIFICATION_FILE, "w") as output_file:
        json.dump(classification, output_file)

    print("Done.")