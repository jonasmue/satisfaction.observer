import json
from typing import List
from datetime import datetime
from .country import Country


class Leader:
    def __init__(self, name: str, image: str, country: Country, since: datetime, until: datetime,
                 searchFirstName=False):
        self.name = name
        self.image = image
        self.country = country
        self.since = since
        self.until = until
        self.search_first_name = searchFirstName


class LeaderFactory:
    @staticmethod
    def get_leaders(file_path: str) -> List[Leader]:
        with open(file_path, "r") as input_file:
            leader_dict = json.load(input_file)

        result = []
        for item in leader_dict["leaders"]:
            leader = item["leader"]
            name = leader["name"]
            image = leader["image"]
            since = datetime.strptime(leader["since"], "%Y-%m-%d")
            until = datetime.strptime(leader["until"], "%Y-%m-%d") if leader["until"] is not None else None
            country_item = leader["country"]
            country = Country(country_item["name"], country_item["locale"], country_item["flag"])
            search_first_name = leader["firstName"] if "firstName" in leader.keys() else False
            result.append(Leader(name, image, country, since, until, search_first_name))

        return result
