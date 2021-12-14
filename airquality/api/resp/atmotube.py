######################################################
#
# Author: Davide Colombo
# Date: 28/11/21 19:21
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any, List
import airquality.api.resp.abc as respabc
import airquality.types.timest as tstype
import airquality.types.postgis as pgistype


# ------------------------------- AtmotubeAPIRespType ------------------------------- #
class AtmotubeAPIRespType(respabc.MeasureAPIRespTypeABC):

    def __init__(
            self, item: Dict[str, Any], measure_param: List[str], timestamp_cls=tstype.AtmotubeSQLTimest, postgis_cls=pgistype.PostgisPoint
    ):
        self.measure_param = measure_param
        self.item = item
        self.timestamp_cls = timestamp_cls
        self.postgis_cls = postgis_cls

    def measured_at(self) -> tstype.TimestABC:
        try:
            time = self.item['time']
            return self.timestamp_cls(timest=time)
        except KeyError as err:
            raise SystemExit(f"{self.__class__.__name__} catches {err.__class__.__name__} exception in {self.measured_at.__name__} => {err!r}")

    def measures(self) -> List[respabc.NameValue]:
        try:
            return [respabc.NameValue(name=param, value=self.item.get(param)) for param in self.measure_param]
        except KeyError as err:
            raise SystemExit(f"{self.__class__.__name__} catches {err.__class__.__name__} exception in {self.measures.__name__} => {err!r}")

    def located_at(self) -> pgistype.PostgisABC:
        try:
            coords = self.item.get('coords')
            return self.postgis_cls(lat=coords['lat'], lng=coords['lon']) if coords is not None else pgistype.NullGeometry()
        except KeyError as err:
            raise SystemExit(f"{self.__class__.__name__} catches {err.__class__.__name__} exception in {self.located_at.__name__} => {err!r}")


# ------------------------------- AtmotubeAPIRespBuilder ------------------------------- #
class AtmotubeAPIRespBuilder(respabc.APIRespBuilderABC):

    CHANNEL_FIELDS = {"main": ["voc", "pm1", "pm25", "pm10", "t", "h", "p"]}

    def __init__(self, channel_name: str, timestamp_cls=tstype.AtmotubeSQLTimest, postgis_cls=pgistype.PostgisPoint):
        self.channel_name = channel_name
        self.timestamp_cls = timestamp_cls
        self.postgis_cls = postgis_cls

    ################################ build() ################################
    def build(self, parsed_resp: Dict[str, Any]) -> List[AtmotubeAPIRespType]:
        try:
            data = parsed_resp['data']
            items = data['items']
            measure_param = self.CHANNEL_FIELDS[self.channel_name]
            return [AtmotubeAPIRespType(item=item, measure_param=measure_param, timestamp_cls=self.timestamp_cls, postgis_cls=self.postgis_cls)
                    for item in items]
        except KeyError as kerr:
            raise SystemExit(f"{self.__class__.__name__} catches {kerr.__class__.__name__} exception in {self.build.__name__} => {kerr!r}")
