######################################################
# 
# Author: Davide Colombo
# Date: 19/12/21 14:28
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from airquality.respitem import AtmotubeItem, PurpleairItem
from collections.abc import Iterable
from typing import List, Generator
from urllib.request import urlopen
from datetime import datetime
from json import loads


###################################### AtmotubeResponses(Iterable) ######################################
class AtmotubeResponses(Iterable):

    def __init__(self, url: str, filter_ts: datetime):
        self.filter_ts = filter_ts
        with urlopen(url) as resp:
            self.parsed = loads(resp.read())

    def __getitem__(self, index) -> AtmotubeItem:
        if index >= len(self):
            raise IndexError(f"{type(self).__name__} index {index} out of range")
        return AtmotubeItem(self.parsed['data']['items'][index])

    def __iter__(self) -> Generator[AtmotubeItem, None, None]:
        items = (AtmotubeItem(item) for item in self.parsed['data']['items'])
        for item in items:
            if item > self.filter_ts:
                yield item

    def __len__(self):
        items = (AtmotubeItem(item) for item in self.parsed['data']['items'])
        return sum(1 for item in items if item.measured_at_datetime > self.filter_ts)


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
