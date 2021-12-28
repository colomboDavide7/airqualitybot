######################################################
#
# Author: Davide Colombo
# Date: 28/12/21 19:51
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Generator, Set
from datetime import datetime
from airquality.iterabc import IterableItemsABC
from airquality.response import AtmotubeAPIResponses, PurpleairAPIResponses
from airquality.respitem import AtmotubeItem, PurpleairItem


class AtmotubeFilteredResponses(IterableItemsABC):

    def __init__(self, responses: AtmotubeAPIResponses, filter_ts: datetime):
        self.responses = responses
        self.filter_ts = filter_ts

    def items(self) -> Generator[AtmotubeItem, None, None]:
        return (item for item in self.responses if item > self.filter_ts)


class PurpleairFilteredResponses(IterableItemsABC):

    def __init__(self, responses: PurpleairAPIResponses, database_sensor_names: Set[str]):
        self.responses = responses
        self.database_sensor_names = database_sensor_names

    def items(self) -> Generator[PurpleairItem, None, None]:
        return (item for item in self.responses if item.name not in self.database_sensor_names)
