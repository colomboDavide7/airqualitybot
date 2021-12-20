######################################################
# 
# Author: Davide Colombo
# Date: 19/12/21 14:28
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from airquality.respitem import AtmotubeItem, PurpleairItem, ThingspeakItem
from collections.abc import Iterable
from typing import List, Generator, Dict
from urllib.request import urlopen
from datetime import datetime
from itertools import islice
from json import loads


###################################### AtmotubeResponses(Iterable) ######################################
class AtmotubeResponses(Iterable):

    def __init__(self, url: str, filter_ts: datetime):
        self.filter_ts = filter_ts
        with urlopen(url) as resp:
            self.parsed = loads(resp.read())

    @property
    def items(self):
        return (AtmotubeItem(item) for item in self.parsed['data']['items'])

    @property
    def filtered_items(self):
        return (item for item in self.items if item > self.filter_ts)

    def __getitem__(self, index) -> AtmotubeItem:
        if index >= len(self):
            raise IndexError(f"{type(self).__name__} in __getitem__(): index '{index}' out of range")
        return next(islice(self.filtered_items, index, None))

    def __iter__(self) -> Generator[AtmotubeItem, None, None]:
        return self.filtered_items

    def __len__(self):
        return sum(1 for item in self.filtered_items)


###################################### PurpleairResponses(Iterable) ######################################
class PurpleairResponses(Iterable):

    def __init__(self, url: str, existing_names: List[str]):
        self.existing_names = existing_names
        with urlopen(url) as resp:
            resp = loads(resp.read())
            self.fields = resp['fields']
            self.data = resp['data']

    def __iter__(self) -> Generator[PurpleairItem, None, None]:
        items = (PurpleairItem(dict(zip(self.fields, d))) for d in self.data)
        for item in items:
            if item.name not in self.existing_names:
                yield item

    def __len__(self):
        items = (PurpleairItem(dict(zip(self.fields, d))) for d in self.data)
        return sum(1 for item in items if item.name not in self.existing_names)


###################################### ThingspeakResponses(Iterable) ######################################
class ThingspeakResponses(Iterable):

    def __init__(self, url: str, filter_ts: datetime, field_map: Dict[str, str]):
        self.field_map = field_map
        self.filter_ts = filter_ts
        with urlopen(url) as resp:
            parsed = loads(resp.read())
            self.feeds = parsed['feeds']

    def __getitem__(self, index) -> ThingspeakItem:
        if index >= len(self):
            raise IndexError(f"{type(self).__name__} in __getitem__(): index '{index}' out of range")
        return ThingspeakItem(item=self.feeds[index], field_map=self.field_map)

    def __iter__(self) -> Generator[ThingspeakItem, None, None]:
        items = (ThingspeakItem(item, field_map=self.field_map) for item in self.feeds)
        for item in items:
            if item > self.filter_ts:
                yield item

    def __len__(self):
        items = (ThingspeakItem(item, field_map=self.field_map) for item in self.feeds)
        return sum(1 for item in items if item > self.filter_ts)
