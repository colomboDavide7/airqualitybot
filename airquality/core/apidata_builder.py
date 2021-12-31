######################################################
#
# Author: Davide Colombo
# Date: 29/12/21 20:12
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from json import loads
from typing import Generator
from urllib.request import urlopen
from airquality.core.iteritems import IterableItemsABC
from airquality.datamodel.apidata import PurpleairAPIData, AtmotubeAPIData


class PurpleairAPIDataBuilder(IterableItemsABC):
    """
    An *IterableItemsABC* that defines the business rules
    for fetching data from Purpleair API and build a *PurpleairDatamodel*.
    """

    def __init__(self, url: str):
        with urlopen(url) as http_response:
            parsed = loads(http_response.read())
            self.fields = parsed['fields']
            self.data = parsed['data']

    def items(self) -> Generator[PurpleairAPIData, None, None]:
        return (PurpleairAPIData(**(dict(zip(self.fields, data)))) for data in self.data)


class AtmotubeAPIDataBuilder(IterableItemsABC):
    """
    An *IterableItemsABC* that defines the business rules
    for fetching data from Atmotube API and build an *AtmotubeDatamodel*.
    """

    def __init__(self, url: str):
        with urlopen(url) as http_response:
            parsed = loads(http_response.read())
            self.api_items = parsed['data']['items']

    def items(self) -> Generator[AtmotubeAPIData, None, None]:
        return (AtmotubeAPIData(**item) for item in self.api_items)
