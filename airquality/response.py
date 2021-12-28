######################################################
# 
# Author: Davide Colombo
# Date: 19/12/21 14:28
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import json
import urllib.request
from typing import Generator
from airquality.iterabc import IterableItemsABC
from airquality.respitem import AtmotubeItem, PurpleairItem, ThingspeakItem


###################################### AtmotubeResponses(IterableItemsABC) ######################################
class AtmotubeAPIResponses(IterableItemsABC):

    def __init__(self, url: str, item_factory=AtmotubeItem):
        self.item_factory = item_factory
        with urllib.request.urlopen(url) as resp:
            self.parsed = json.loads(resp.read())

    def items(self) -> Generator[AtmotubeItem, None, None]:
        return (self.item_factory(item) for item in self.parsed['data']['items'])


###################################### PurpleairResponses(IterableItemsABC) ######################################
class PurpleairAPIResponses(IterableItemsABC):

    def __init__(self, url: str, item_factory=PurpleairItem):
        self.item_factory = item_factory
        with urllib.request.urlopen(url) as resp:
            resp = json.loads(resp.read())
            self.fields = resp['fields']
            self.data = resp['data']

    def items(self) -> Generator[PurpleairItem, None, None]:
        return (self.item_factory(dict(zip(self.fields, d))) for d in self.data)


# ###################################### ThingspeakResponses(Iterable) ######################################
# class ThingspeakResponse(APIResponse):
#
#     def __init__(self, url: str, filter_ts: datetime, field_map: Dict[str, str], item_factory=ThingspeakItem):
#         super(ThingspeakResponse, self).__init__(item_factory=item_factory)
#         self.field_map = field_map
#         self.filter_ts = filter_ts
#         with urlopen(url) as resp:
#             parsed = loads(resp.read())
#             self.feeds = parsed['feeds']
#
#     def items(self) -> Generator[ThingspeakItem, None, None]:
#         return (self.item_factory(item, field_map=self.field_map) for item in self.feeds)
#
#     def filtered_items(self) -> Generator[ThingspeakItem, None, None]:
#         return (item for item in self.items() if item > self.filter_ts)
