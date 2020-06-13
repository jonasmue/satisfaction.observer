import numpy as np

import os
import json
from datetime import datetime, timedelta

TIME_DELTA_DAYS = 7
POPULAR = False
THRESHOLD = 0.65

DATE = (datetime.now() - timedelta(days=TIME_DELTA_DAYS)).strftime("%Y-%m-%d")


DATA_DIR = os.path.join("..", "_data")
ANALYZED_DATA_DIR = os.path.join(DATA_DIR, "analyzed")
MEAN_NORM_DATA_DIR = os.path.join(DATA_DIR, "mean_norm")

popular_suffix = "_popular" if POPULAR else ""
CLASSIFICATION_FILE = os.path.join(ANALYZED_DATA_DIR, DATE + popular_suffix + "_classifications.json")
OUTPUT_FILE = os.path.join(MEAN_NORM_DATA_DIR, DATE + popular_suffix + "_classifications-mean-normalized.json")

print("Opening", CLASSIFICATION_FILE, "...")
with open(CLASSIFICATION_FILE, "r") as input_file:
    classification = json.load(input_file)

print("Calculating mean values...")
mean_normalized_classifications = {}
for leader in classification.keys():
    classifications = [c[0] for c in classification[leader] if c[1] > THRESHOLD]
    weights = [c[1] for c in classification[leader] if c[1] > THRESHOLD]
    assert len(classifications) == len(weights)
    print(len(classifications), "items for", leader)
    mean_normalized_classifications[leader] = np.average(classifications, weights=weights) * 100 / 5

print("Done. Saving mean values to", OUTPUT_FILE, "...")
with open(OUTPUT_FILE, "w") as output_file:
    json.dump(mean_normalized_classifications, output_file)
print("Done.")
