######################################################
#
# Author: Davide Colombo
# Date: 28/11/21 19:21
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any, List
import airquality.source.api.resp.abc as respabc

CHANNEL_FIELDS = {"main": ["voc", "pm1", "pm25", "pm10", "t", "h", "p"]}


# ------------------------------- AtmotubeAPIRespType ------------------------------- #
class AtmotubeAPIRespType(respabc.APIRespTypeABC):

    def __init__(self, item: Dict[str, Any], channel_name: str):
        self.channel_name = channel_name
        self.item = item

    @property
    def time(self) -> str:
        return self.item['time']

    @property
    def geolocation(self) -> respabc.SensorGeolocation or None:
        coords = self.item.get('coords')
        return respabc.SensorGeolocation(latitude=coords['lat'], longitude=coords['lon']) if coords is not None else None

    @property
    def measures(self) -> List[respabc.NameValue]:
        channel_field_map = CHANNEL_FIELDS[self.channel_name]
        return [respabc.NameValue(name=param, value=self.item.get(param)) for param in channel_field_map]


# ------------------------------- AtmotubeAPIRespBuilder ------------------------------- #
class AtmotubeAPIRespBuilder(respabc.APIRespBuilderABC):

    def __init__(self, channel_name: str):
        self.channel_name = channel_name

    ################################ build() ################################
    def build(self, parsed_resp: Dict[str, Any]) -> List[AtmotubeAPIRespType]:
        try:
            data = parsed_resp['data']
            items = data['items']
            return [AtmotubeAPIRespType(item=item, channel_name=self.channel_name) for item in items]
        except KeyError as kerr:
            raise SystemExit(f"{self.__class__.__name__} catches {kerr.__class__.__name__} => {kerr!s}")
