import json

import numpy as np


class MeanCalculator:
    def __init__(self, source_file, target_file, threshold):
        self.source_file = source_file
        self.target_file = target_file
        self.threshold = threshold

    def run(self):
        with open(self.source_file, "r") as input_file:
            classification = json.load(input_file)

        mean_normalized_classifications = {}

        for leader in classification.keys():
            classifications = [c[0] - 1 for c in classification[leader] if c[1] > self.threshold]
            weights = [c[1] for c in classification[leader] if c[1] > self.threshold]
            assert len(classifications) == len(weights)
            print(len(classifications), "items for", leader)
            mean_normalized_classifications[leader] = np.average(classifications, weights=weights) * 100 / 4

        with open(self.target_file, "w") as output_file:
            json.dump(mean_normalized_classifications, output_file)
