import os
import json
import numpy as np
from transformers import *
from tqdm import tqdm

DATE = "2020-06-05"

DATA_DIR = os.path.join("..", "_data")
ANALYZED_DATA_DIR = os.path.join(DATA_DIR, "analyzed")

RAW_FILE = os.path.join(DATA_DIR, "raw", DATE + ".json")
CLASSIFICATION_FILE = os.path.join(ANALYZED_DATA_DIR, DATE + "_classifications.json")
OUTPUT_FILE = os.path.join(ANALYZED_DATA_DIR, DATE + "_classifications-mean-normalized.json")

tokenizer = AutoTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
model = AutoModelForSequenceClassification.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
sentiment_analyzer = TextClassificationPipeline(model=model, tokenizer=tokenizer)

with open(RAW_FILE, "r") as input_file:
    tweets = json.load(input_file)

classification = {}
for leader, leader_tweets in tweets.items():
    classification[leader] = []
    for tweet in tqdm(leader_tweets):
        c = sentiment_analyzer(tweet)[0]
        classification[leader].append((int(c["label"].split()[0]), c["score"]))

with open(CLASSIFICATION_FILE, "w") as output_file:
    json.dump(classification, output_file)

mean_normalized_classifications = {}
for leader in classification.keys():
    classifications = [c[0] for c in classification[leader]]
    weights = [c[1] for c in classification[leader]]
    mean_normalized_classifications[leader] = np.average(classifications, weights=weights) * 100 / 5

with open(OUTPUT_FILE, "w") as output_file:
    json.dump(mean_normalized_classifications, output_file)
