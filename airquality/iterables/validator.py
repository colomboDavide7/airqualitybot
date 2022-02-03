######################################################
#
# Author: Davide Colombo
# Date: 30/12/21 11:10
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from airquality.iterables.abc import IterableItemsABC
from typing import Generator, Set
from datetime import datetime


class FixedSensorIterableValidRequests(IterableItemsABC):
    """
    A class that implements the *IterableItemsABC* interface and filter out requests based their name.
    """

    def __init__(self, request: IterableItemsABC, name2remove: Set[str]):
        self.request = request
        self.name2remove = name2remove

    def items(self) -> Generator:
        for request in self.request:
            if request.name not in self.name2remove:
                yield request


class SensorMeasureIterableValidRequests(IterableItemsABC):
    """
    A class that implements the *IterableItemsABC* interface and filter out requests based on time criteria.
    """

    def __init__(self, requests: IterableItemsABC, filter_ts: datetime):
        self.request = requests
        self.filter_ts = filter_ts

    def items(self) -> Generator:
        for request in self.request:
            if request.timestamp > self.filter_ts:
                yield request


class PlaceIterableValidRequests(IterableItemsABC):
    """
    A class that implements the *IterableItemsABC* interface and filter out requests based their postcode.
    """

    def __init__(self, requests: IterableItemsABC, postcodes2remove: Set[str]):
        self.requests = requests
        self.postcodes2remove = postcodes2remove

    def items(self) -> Generator:
        for request in self.requests:
            if request.poscode not in self.postcodes2remove:
                yield request
