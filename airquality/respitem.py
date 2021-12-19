######################################################
#
# Author: Davide Colombo
# Date: 19/12/21 14:30
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
SQL_DATETIME_FMT = "%Y-%m-%d %H:%M:%S"
ST_GEOM_FROM_TEXT = "ST_GeomFromText('{geom}', {srid})"
POSTGIS_POINT = "POINT({lon} {lat})"


from typing import Dict, Any, Set, List, Tuple
from collections import namedtuple
from datetime import datetime


###################################### AtmotubeItem(object) ######################################
class AtmotubeItem(object):
    ATMOTUBE_MEASURE_PARAM = ['voc', 'pm1', 'pm25', 'pm10', 't', 'h', 'p']

    def __init__(self, item: Dict[str, Any]):
        self.item = item
        self._at = ""
        self._coords = ""
        self._at_datetime = ""

    def __gt__(self, other):
        if not isinstance(other, datetime):
            raise TypeError(f"{type(self).__name__} in __gt__(): expected 'datetime' object, got {type(other).__name__}")
        return (self.measured_at_datetime - other).total_seconds() > 0

    @property
    def measured_at_datetime(self) -> datetime:
        if not self._at_datetime:
            self._at_datetime = datetime.strptime(self.measured_at, SQL_DATETIME_FMT)
        return self._at_datetime

    @property
    def measured_at(self) -> str:
        if not self._at:
            self._at = self.item['time'].replace("T", " ").split('.')[0]
        return self._at

    @property
    def coords(self):
        if not self._coords:
            tmp = self.item.pop('coords', None)
            self._coords = "NULL"
            if tmp is not None:
                pt = POSTGIS_POINT.format(lat=tmp['lat'], lon=tmp['lon'])
                self._coords = ST_GEOM_FROM_TEXT.format(geom=pt, srid=26918)
        return self._coords

    @property
    def values(self) -> List[Tuple[str, Any]]:
        return [(pcode, self.item.get(pcode)) for pcode in self.ATMOTUBE_MEASURE_PARAM]


###################################### ChannelProperties(namedtuple) ######################################
class ChannelProperties(namedtuple('ChannelProperties', ['key', 'ident', 'name'])):

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name}, key=XXX, ident=XXX)"


###################################### PurpleairItem(object) ######################################
class PurpleairItem(object):
    CHANNELS_PARAM = [{'key': 'primary_key_a', 'ident': 'primary_id_a', 'name': '1A'},
                      {'key': 'primary_key_b', 'ident': 'primary_id_b', 'name': '1B'},
                      {'key': 'secondary_key_a', 'ident': 'secondary_id_a', 'name': '2A'},
                      {'key': 'secondary_key_b', 'ident': 'secondary_id_b', 'name': '2B'}]

    def __init__(self, item: Dict[str, Any]):
        self.item = item
        self._channels = set()
        self._geom = ""
        self._name = ""
        self._at = ""

    @property
    def name(self) -> str:
        if not self._name:
            self._name = f"{self.item['name']} ({self.item['sensor_index']})"
        return self._name

    @property
    def type(self) -> str:
        return "Purpleair/Thingspeak"

    @property
    def located_at(self) -> str:
        if not self._geom:
            point = POSTGIS_POINT.format(lon=self.item['longitude'], lat=self.item['latitude'])
            self._geom = ST_GEOM_FROM_TEXT.format(geom=point, srid=26918)
        return self._geom

    @property
    def created_at(self) -> str:
        if not self._at:
            self._at = datetime.fromtimestamp(self.item['date_created']).strftime(SQL_DATETIME_FMT)
        return self._at

    @property
    def channel_properties(self) -> Set[ChannelProperties]:
        if not self._channels:
            self._channels = {ChannelProperties(key=self.item[p['key']], ident=self.item[p['ident']], name=p['name'])
                              for p in self.CHANNELS_PARAM}
        return self._channels

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name}, created_at={self.created_at}, located_at={self.located_at}, " \
               f"channels={self.channel_properties!r})"
