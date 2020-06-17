import os
from analysis.mean_calculator import MeanCalculator

analyzed_dir = os.path.join("..", "_data", "analyzed")
target_dir = os.path.join("..", "display", "data")
for file_name in os.listdir(analyzed_dir):
    is_popular = "popular" in file_name
    source_file = os.path.join(analyzed_dir, file_name)
    target_file = os.path.join(target_dir, "popular", file_name) if is_popular else os.path.join(target_dir, "recent", file_name)
    MeanCalculator(source_file, target_file, 0.65).run()