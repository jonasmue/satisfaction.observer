import json


class ExampleExtractor:
    def __init__(self, source_file, classifications_file, target_file, extract_num=1):
        self.source_file = source_file
        self.classifications_file = classifications_file
        self.target_file = target_file
        self.extract_num = extract_num

    def run(self):
        with open(self.source_file, "r") as input_file:
            tweets = json.load(input_file)
        with open(self.classifications_file, "r") as input_file:
            classifications = json.load(input_file)

        result = {}
        for leader, classification_list in classifications.items():
            result[leader] = {}
            five_star_classifications = {i: c[1] for i, c in enumerate(classification_list) if c[0] == 5}
            one_star_classifications = {i: c[1] for i, c in enumerate(classification_list) if c[0] == 1}

            five_star_classifications = {k: v for k, v in
                                         sorted(five_star_classifications.items(), key=lambda item: item[1])}
            one_star_classifications = {k: v for k, v in
                                        sorted(one_star_classifications.items(), key=lambda item: item[1])}

            max_five_star = list(five_star_classifications.keys())[-self.extract_num:]
            max_one_star = list(one_star_classifications.keys())[-self.extract_num:]

            result[leader]["pos"] = [tweets[leader][t] for t in max_five_star]
            result[leader]["neg"] = [tweets[leader][t] for t in max_one_star]

        with open(self.target_file, "w") as output_file:
            json.dump(result, output_file)
