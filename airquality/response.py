######################################################
# 
# Author: Davide Colombo
# Date: 19/12/21 14:28
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from airquality.respitem import AtmotubeItem
from collections.abc import Iterable
from typing import List, Generator
from urllib.request import urlopen
from datetime import datetime
from json import loads


class AtmotubeResponses(Iterable):

    def __init__(self, url: str, items_of_interest: List[str], filter_ts: datetime, default=None):
        self.items_of_interest = items_of_interest
        self.default = default
        self.filter_ts = filter_ts
        self.url = url
        with urlopen(self.url) as resp:
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
