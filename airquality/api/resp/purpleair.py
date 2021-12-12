######################################################
#
# Author: Davide Colombo
# Date: 28/11/21 18:55
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List, Dict, Any
import airquality.api.resp.abc as respabc
import airquality.types.timestamp as tstype
import airquality.types.postgis as pgistype

CHANNEL_PARAM = [{'name': 'Primary data - Channel A', 'key': 'primary_key_a', 'id': 'primary_id_a'},
                 {'name': 'Primary data - Channel B', 'key': 'primary_key_b', 'id': 'primary_id_b'},
                 {'name': 'Secondary data - Channel A', 'key': 'secondary_key_a', 'id': 'secondary_id_a'},
                 {'name': 'Secondary data - Channel B', 'key': 'secondary_key_b', 'id': 'secondary_id_b'}]


# ------------------------------- PurpleairAPIRespType ------------------------------- #
class PurpleairAPIRespType(respabc.InfoAPIRespTypeABC):

    def __init__(self, item: Dict[str, Any], timestamp_cls=tstype.UnixTimestamp, postgis_cls=pgistype.PostgisPoint):
        self.item = item
        self.timestamp_cls = timestamp_cls
        self.postgis_cls = postgis_cls

    def date_created(self) -> tstype.Timestamp:
        try:
            date = self.item['date_created']
            return self.timestamp_cls(timest=date)
        except KeyError as kerr:
            raise SystemExit(f"{self.__class__.__name__} in {self.date_created.__name__} catches {kerr.__class__.__name__} exception => {kerr!r}")

    def sensor_type(self) -> str:
        return "Purpleair/Thingspeak"

    def sensor_name(self) -> str:
        try:
            name = self.item['name'].replace("'", "")
            sensor_index = self.item['sensor_index']
            return f"{name} ({sensor_index})"
        except KeyError as kerr:
            raise SystemExit(f"{self.__class__.__name__} in {self.sensor_name.__name__} catches {kerr.__class__.__name__} exception => {kerr!r}")

    def geolocation(self) -> pgistype.PostgisPoint:
        try:
            latitude = self.item['latitude']
            longitude = self.item['longitude']
            return self.postgis_cls(lat=latitude, lng=longitude)
        except KeyError as kerr:
            raise SystemExit(f"{self.__class__.__name__} in {self.geolocation.__name__} catches {kerr.__class__.__name__} exception => {kerr!r}")

    def channels(self) -> List[respabc.ChannelParam]:
        try:
            return [respabc.ChannelParam(key=self.item[param['key']], ident=self.item[param['id']], name=param['name']) for param in CHANNEL_PARAM]
        except KeyError as kerr:
            raise SystemExit(f"{self.__class__.__name__} in {self.channels.__name__} catches {kerr.__class__.__name__} exception => {kerr!r}")


# ------------------------------- PurpleairAPIRespBuilder ------------------------------- #
class PurpleairAPIRespBuilder(respabc.APIRespBuilderABC):

    def __init__(self, timestamp_cls=tstype.UnixTimestamp, postgis_cls=pgistype.PostgisPoint):
        self.timestamp_cls = timestamp_cls
        self.postgis_cls = postgis_cls

    ################################ build() ################################
    def build(self, parsed_resp: Dict[str, Any]) -> List[PurpleairAPIRespType]:
        try:
            fields = parsed_resp['fields']
            data = parsed_resp['data']
            return [PurpleairAPIRespType(item=dict(zip(fields, d)), timestamp_cls=self.timestamp_cls, postgis_cls=self.postgis_cls) for d in data]
        except KeyError as kerr:
            raise SystemExit(f"{self.__class__.__name__} catches {kerr.__class__.__name__} => {kerr!r}")
