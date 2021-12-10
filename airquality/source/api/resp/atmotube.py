######################################################
#
# Author: Davide Colombo
# Date: 28/11/21 19:21
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any, List
import airquality.source.api.resp.abc as respabc


# ------------------------------- AtmotubeAPIRespType ------------------------------- #
class AtmotubeAPIRespType(respabc.APIRespTypeABC):

    def __init__(self, item: Dict[str, Any], measure_param: List[str]):
        self.measure_param = measure_param
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
        return [respabc.NameValue(name=param, value=self.item.get(param)) for param in self.measure_param]


# ------------------------------- AtmotubeAPIRespBuilder ------------------------------- #
class AtmotubeAPIRespBuilder(respabc.APIRespBuilderABC):

    CHANNEL_FIELDS = {"main": ["voc", "pm1", "pm25", "pm10", "t", "h", "p"]}

    def __init__(self, channel_name: str):
        self.channel_name = channel_name

    ################################ build() ################################
    def build(self, parsed_resp: Dict[str, Any]) -> List[AtmotubeAPIRespType]:
        try:
            data = parsed_resp['data']
            items = data['items']
            measure_param = self.CHANNEL_FIELDS[self.channel_name]
            return [AtmotubeAPIRespType(item=item, measure_param=measure_param) for item in items]
        except KeyError as kerr:
            raise SystemExit(f"{self.__class__.__name__} catches {kerr.__class__.__name__} => {kerr!s}")
