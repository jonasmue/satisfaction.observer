import json
from typing import List, Dict
from datetime import datetime
from .country import Country


class Item:
    """
    An item is a canonical element of a category.
    """

    def __init__(self, name: str, country: Country, since: datetime, until: datetime,
                 search_term: str):
        """
        :param name: The item's name
        :param country: The <code>Country</code> where the item is located
        :param since: Start date of item
        :param until: End date of item, or <code>None</code> if ongoing
        :param search_term: Determines the term that is supposed to be searched for
        """
        self.name = name
        self.country = country
        self.since = since
        self.until = until
        self.search_term = search_term


class ItemFactory:
    """
    Factory responsible for generation of <code>Leader</code> objects
    """

    @staticmethod
    def get_items(file_path: str) -> (List[Item], Dict[str, str]):
        """
        Parses given file and returns list of <code>Item</code> objects represented in the file.

        :param file_path: The file where the <code>Item</code>s are annotated (must be a JSON file!)
        :return: A list of of <code>Item</code> objects, and a dictionary mapping from a locale to a replacement word
        """
        with open(file_path, "r") as input_file:
            item_dict = json.load(input_file)

        result = []
        for element in item_dict["items"]:
            item = element["item"]
            name = item["name"]
            since = datetime.strptime(item["since"], "%Y-%m-%d") if item["since"] is not None else None
            until = datetime.strptime(item["until"], "%Y-%m-%d") if item["until"] is not None else None
            country_item = item["country"]
            country = Country(country_item["name"], country_item["locale"])
            search_term = item["searchTerm"] if "searchTerm" in item.keys() else name
            result.append(Item(name, country, since, until, search_term))

        return result, item_dict["cleanReplacement"]
