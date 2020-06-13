import os
import argparse
from time import time
from datetime import datetime, timedelta
from generation.twitter_querier import TwitterQuerier
from generation.text_cleaner import TextCleaner
from analysis.analyzer import SemanticClassificationAnalyzer
from analysis.mean_calculator import MeanCalculator

# SETUP ARGUMENT PARSER AND DEFAULT ARGUMENTS
parser = argparse.ArgumentParser()
parser.add_argument("--time_delta", type=int, default=0,
                    help="The delta of days you want to go back to scrape tweets. Use 0 if yesterday's tweets are to be scraped")
parser.add_argument("--popular", type=bool, default=False,
                    help="Set to true if a mixture of popular and recent tweets are to be scraped, or to False if only recent tweets are to be scraped")
parser.add_argument("--classification_threshold", type=float, default=0.65,
                    help="Determining when confidence of classification is high enough for the respective class to be taken into account for final result calculation")
args = parser.parse_args()

# SETUP PATHS TO DATA DIRECTORIES
data_dir = "_data"
raw_dir = os.path.join(data_dir, "raw")
cleaned_dir = os.path.join(data_dir, "cleaned")
analyzed_dir = os.path.join(data_dir, "analyzed")
mean_norm_dir = os.path.join(data_dir, "mean_norm")

# SETUP FILE NAMES AND PATHS
popular_suffix = "_popular" if args.popular else ""
day_string = (datetime.now() - timedelta(days=args.time_delta)).strftime("%Y-%m-%d")

leaders_file = os.path.join("general", "leaders.json")

file_name = day_string + popular_suffix + ".json"
raw_file = os.path.join(raw_dir, file_name)
cleaned_file = os.path.join(cleaned_dir, file_name)
classification_file = os.path.join(analyzed_dir, file_name)
target_file = os.path.join(mean_norm_dir, file_name)

# EXECUTE ONE DATA SCRAPE AND ANALYSIS PROCEDURE
print("GENERATING DATA FOR {}".format(day_string))
print("-" * 80)
print("-" * 80)

print("Querying Twitter...")
start = time()
TwitterQuerier(raw_file, args.popular, args.time_delta, leaders_file).run()
print("Done. Took {} seconds".format(time() - start))
print("=" * 80)

print("Cleaning Text...")
start = time()
TextCleaner(raw_file, cleaned_file, leaders_file).run()
print("Done. Took {} seconds".format(time() - start))
print("=" * 80)

print("Generating Sentiment Classes...")
start = time()
SemanticClassificationAnalyzer(cleaned_file, classification_file).run()
print("Done. Took {} seconds".format(time() - start))
print("=" * 80)

print("Generating Mean Normalized Values of Classes...")
start = time()
MeanCalculator(classification_file, target_file, args.classification_threshold).run()
print("Done. Took {} seconds".format(time() - start))
print("=" * 80)
