######################################################
#
# Author: Davide Colombo
# Date: 28/11/21 18:55
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List, Dict, Any
import airquality.api.resp.abc as respabc

CHANNEL_PARAM = [{'name': 'Primary data - Channel A', 'key': 'primary_key_a', 'id': 'primary_id_a'},
                 {'name': 'Primary data - Channel B', 'key': 'primary_key_b', 'id': 'primary_id_b'},
                 {'name': 'Secondary data - Channel A', 'key': 'secondary_key_a', 'id': 'secondary_id_a'},
                 {'name': 'Secondary data - Channel B', 'key': 'secondary_key_b', 'id': 'secondary_id_b'}]


# ------------------------------- PurpleairAPIRespType ------------------------------- #
class PurpleairAPIRespType(respabc.APIRespTypeABC):

    def __init__(self, item: Dict[str, Any]):
        self.item = item

    @property
    def sensor_index(self) -> str:
        return self.item['sensor_index']

    @property
    def name(self) -> str:
        return self.item['name']

    @property
    def date_created(self) -> int:
        return self.item['date_created']

    @property
    def channels(self) -> List[respabc.ChannelParam]:
        return [respabc.ChannelParam(key=self.item[param['key']], ident=self.item[param['id']], name=param['name']) for param in CHANNEL_PARAM]

    @property
    def geolocation(self) -> respabc.SensorGeolocation:
        return respabc.SensorGeolocation(latitude=self.item['latitude'], longitude=self.item['longitude'])

    # TODO: create a SQL adapter that takes (this object + sensor_id) and defines the methods for converting responses into SQL


# ------------------------------- PurpleairAPIRespBuilder ------------------------------- #
class PurpleairAPIRespBuilder(respabc.APIRespBuilderABC):

    ################################ build() ################################
    def build(self, parsed_resp: Dict[str, Any]) -> List[PurpleairAPIRespType]:
        try:
            fields = parsed_resp['fields']
            data = parsed_resp['data']
            return [PurpleairAPIRespType(item=dict(zip(fields, d))) for d in data]
        except KeyError as kerr:
            raise SystemExit(f"{self.__class__.__name__} catches {kerr.__class__.__name__} => {kerr!s}")
