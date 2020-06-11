import json
from typing import List
from datetime import datetime
from .country import Country


class Leader:
    """
    A leader is a head of a government.
    """

    def __init__(self, name: str, image: str, country: Country, since: datetime, until: datetime,
                 searchFirstName=False):
        """
        :param name: The leader's name
        :param image: An image depicting the person, or a fallback
        :param country: The <code>Country</code> led by the person
        :param since: Start date of leadership
        :param until: End date of leadership, or <code>None</code> if ongoing
        :param searchFirstName: Determines if the first name should be used for search (<code>True</code>) or not (<code>False</code>)
        """
        self.name = name
        self.image = image
        self.country = country
        self.since = since
        self.until = until
        self.search_first_name = searchFirstName


class LeaderFactory:
    """
    Factory responsible for generation of <code>Leader</code> objects
    """

    @staticmethod
    def get_leaders(file_path: str) -> List[Leader]:
        """
        Parses given file and returns list of <code>Leader</code> objects represented in the file.

        :param file_path: The file where the <code>Leader</code>s are annotated (must be a JSON file!)
        :return: A list of of <code>Leader</code> objects
        """
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
