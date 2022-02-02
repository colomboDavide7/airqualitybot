# ======================================
# @author:  Davide Colombo
# @date:    2022-02-2, mer, 12:51
# ======================================
import json
from typing import Generator
from airquality.iterables.abc import IterableItemsABC
from airquality.datamodel.fromfile import GeonamesDM, CityDM


class GeonamesIterableDatamodels(IterableItemsABC):
    """
    An *IterableItemsABC* that defines the business rules
    for reading geonames data from *filename* and build a
    generator of *GeonamesData*.
    """
    def __init__(self, filepath: str):
        with open(filepath, "r") as f:
            lines = f.read().split('\n')
            self.tokenized = [line.split('\t') for line in lines if line]

    def items(self) -> Generator[GeonamesDM, None, None]:
        return (GeonamesDM(*line) for line in self.tokenized)


class CityIterableDatamodels(IterableItemsABC):
    """
    An *IterableItemsABC* that defines the business rules for reading the city data from a file and
    translate them into a Generator of *WeatherCityData* objects that are used for querying city's information
    from the *geographical_area* table in the database.
    """

    def __init__(self, filepath: str):
        with open(filepath, 'r') as f:
            parsed = json.load(f)
            self.cities = parsed['cities']

    def items(self) -> Generator[CityDM, None, None]:
        return (CityDM(**city) for city in self.cities)
