######################################################
# 
# Author: Davide Colombo
# Date: 19/12/21 14:28
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from airquality.respitem import AtmotubeItem, PurpleairItem, ThingspeakItem
from collections.abc import Iterable
from typing import Set, Dict, Generator
from urllib.request import urlopen
from datetime import datetime
from itertools import islice
from json import loads
from abc import ABC, abstractmethod


class APIResponse(Iterable, ABC):

    def __init__(self, item_factory):
        self.item_factory = item_factory

    @abstractmethod
    def items(self):
        pass

    @abstractmethod
    def filtered_items(self):
        pass

    def __getitem__(self, index):
        if index >= len(self):
            raise IndexError(f"{type(self).__name__} in __getitem__(): index '{index}' out of range")
        return next(islice(self.filtered_items(), index, None))

    def __iter__(self):
        return self.filtered_items()

    def __len__(self):
        return sum(1 for _ in self.filtered_items())


###################################### AtmotubeResponses(APIResponse) ######################################
class AtmotubeResponse(APIResponse):

    def __init__(self, url: str, filter_ts: datetime, item_factory=AtmotubeItem):
        super(AtmotubeResponse, self).__init__(item_factory=item_factory)
        self.filter_ts = filter_ts
        with urlopen(url) as resp:
            self.parsed = loads(resp.read())

    def items(self) -> Generator[AtmotubeItem, None, None]:
        return (self.item_factory(item) for item in self.parsed['data']['items'])

    def filtered_items(self) -> Generator[AtmotubeItem, None, None]:
        return (item for item in self.items() if item > self.filter_ts)


###################################### PurpleairResponses(APIResponse) ######################################
class PurpleairResponse(APIResponse):

    def __init__(self, url: str, existing_names: Set[str], item_factory=PurpleairItem):
        super(PurpleairResponse, self).__init__(item_factory=item_factory)
        self.existing_names = existing_names
        with urlopen(url) as resp:
            resp = loads(resp.read())
            self.fields = resp['fields']
            self.data = resp['data']

    def items(self) -> Generator[PurpleairItem, None, None]:
        return (self.item_factory(dict(zip(self.fields, d))) for d in self.data)

    def filtered_items(self) -> Generator[PurpleairItem, None, None]:
        return (item for item in self.items() if item.name() not in self.existing_names)


###################################### ThingspeakResponses(Iterable) ######################################
class ThingspeakResponse(APIResponse):

    def __init__(self, url: str, filter_ts: datetime, field_map: Dict[str, str], item_factory=ThingspeakItem):
        super(ThingspeakResponse, self).__init__(item_factory=item_factory)
        self.field_map = field_map
        self.filter_ts = filter_ts
        with urlopen(url) as resp:
            parsed = loads(resp.read())
            self.feeds = parsed['feeds']

    def items(self) -> Generator[ThingspeakItem, None, None]:
        return (self.item_factory(item, field_map=self.field_map) for item in self.feeds)

    def filtered_items(self) -> Generator[ThingspeakItem, None, None]:
        return (item for item in self.items() if item > self.filter_ts)
