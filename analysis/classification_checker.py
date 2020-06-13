import json
import os

LEADER = "Angela Merkel"
FILE_NAME = "2020-06-07_classifications.json"
FILE_DIR = os.path.join("..", "_data", "analyzed")
TWEET_NAME = "2020-06-07.json"
TWEET_DIR = os.path.join("..", "_data", "raw")

with open(os.path.join(FILE_DIR, FILE_NAME), "r") as input_file:
    classification_dict = json.load(input_file)

classifications = classification_dict[LEADER]
five_star_classifications = {i:c[1] for i, c in enumerate(classifications) if c[0] == 5}
one_star_classifications = {i:c[1] for i, c in enumerate(classifications) if c[0] == 1}

five_star_classifications = {k: v for k, v in sorted(five_star_classifications.items(), key=lambda item: item[1])}
one_star_classifications = {k: v for k, v in sorted(one_star_classifications.items(), key=lambda item: item[1])}


max_five_star = list(five_star_classifications.keys())[-5:]
max_one_star = list(one_star_classifications.keys())[-5:]

with open(os.path.join(TWEET_DIR, TWEET_NAME), "r") as input_file:
    tweets = json.load(input_file)

for r in max_five_star:
    print("Max 5 Star:", tweets[LEADER][r], "Confidence:", five_star_classifications[r])
    print("-" * 80)

print("=" * 80)

for r in max_one_star:
    print("Max 1 Star:", tweets[LEADER][r], "Confidence:", one_star_classifications[r])
    print("-" * 80)

