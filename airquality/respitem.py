######################################################
#
# Author: Davide Colombo
# Date: 19/12/21 14:30
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any, Set, Tuple
from collections import namedtuple
from datetime import datetime


###################################### AtmotubeItem(object) ######################################
class AtmotubeItem(object):

    ATMOTUBE_MEASURE_PARAM = ['voc', 'pm1', 'pm25', 'pm10', 't', 'h', 'p']
    ATMOTUBE_TIMESTAMP = "%Y-%m-%dT%H:%M:%S.000Z"

    def __init__(self, item: Dict[str, Any]):
        self.item = item

    def __gt__(self, other) -> bool:
        if not isinstance(other, datetime):
            raise TypeError(f"{type(self).__name__} expected '{type(other)}' to be a '{datetime.__class__.__name__}'")
        return datetime.strptime(self.time, self.ATMOTUBE_TIMESTAMP) > other

    @property
    def time(self) -> str:
        return self.item['time']

    @property
    def coords(self):
        return self.item.get('coords')

    @property
    def values(self) -> Set[Tuple[str, Any]]:
        return {(pcode, self.item.get(pcode)) for pcode in self.ATMOTUBE_MEASURE_PARAM}

    def __repr__(self):
        return f"{type(self).__name__}(time={self.time}, values={self.values!r}, coords={self.coords})"


###################################### Channel(namedtuple) ######################################
class Channel(namedtuple('Channel', ['key', 'ident', 'name'])):

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name}, key=XXX, ident=XXX)"


###################################### PurpleairItem(object) ######################################
class PurpleairItem(object):
    CHANNELS = [{'key': 'primary_key_a', 'ident': 'primary_id_a', 'name': '1A'},
                {'key': 'primary_key_b', 'ident': 'primary_id_b', 'name': '1B'},
                {'key': 'secondary_key_a', 'ident': 'secondary_id_a', 'name': '2A'},
                {'key': 'secondary_key_b', 'ident': 'secondary_id_b', 'name': '2B'}]

    def __init__(self, item: Dict[str, Any]):
        self.item = item
        self._name = ""

    @property
    def name(self) -> str:
        if not self._name:
            self._name = f"{self.item['name']} ({self.item['sensor_index']})"
        return self._name

    @property
    def channels(self) -> Set[Channel]:
        return {Channel(key=self.item[c['key']], ident=self.item[c['ident']], name=c['name']) for c in self.CHANNELS}

    @property
    def latitude(self) -> float:
        return self.item['latitude']

    @property
    def longitude(self) -> float:
        return self.item['longitude']

    @property
    def date_created(self) -> int:
        return self.item['date_created']

    def __repr__(self):
        return f"{type(self).__name__}(name={self.name}, channels={self.channels!r}, " \
               f"latitude={self.latitude}, longitude={self.longitude}, date_created={self.date_created})"


###################################### ThingspeakItem(object) ######################################
class ThingspeakItem(object):

    def __init__(self, item: Dict[str, Any], field_map: Dict[str, str]):
        self.item = item
        self.field_map = field_map
        self._at = ""
        self._at_datetime = None

    def measured_at_datetime(self) -> datetime:
        if self._at_datetime is None:
            self._at_datetime = datetime.strptime(self.measured_at(), SQL_DATETIME_FMT)
        return self._at_datetime

    def measured_at(self) -> str:
        if not self._at:
            self._at = self.item['created_at'].replace("T", " ").strip("Z")
        return self._at

    def values(self) -> Set[Tuple[str, Any]]:
        return {(self.field_map[f], self.item.get(f)) for f in self.field_map}

    def __repr__(self):
        return f"{type(self).__name__}(created_at={self.measured_at()}, values={self.values()!r})"
