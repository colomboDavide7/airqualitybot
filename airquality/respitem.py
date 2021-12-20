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


from typing import Dict, Any, Set, Tuple
from collections import namedtuple
from datetime import datetime
from abc import ABC, abstractmethod


###################################### ChannelProperties(namedtuple) ######################################
class ChannelProperties(namedtuple('ChannelProperties', ['key', 'ident', 'name'])):

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name}, key=XXX, ident=XXX)"


class ItemWithIdentityABC(ABC):

    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def type(self) -> str:
        pass

    @abstractmethod
    def channel_properties(self) -> Set[ChannelProperties]:
        pass

    @abstractmethod
    def created_at(self) -> str:
        pass

    def __repr__(self):
        return f"{type(self).__name__}(name={self.name()}, type={self.type()}, created_at={self.created_at}, " \
               f"channels={self.channel_properties()!r})"


class ItemWithLocationABC(ABC):

    @abstractmethod
    def located_at(self) -> str:
        pass

    def __repr__(self):
        return f"{type(self).__name__}(located_at={self.located_at()})"


class ItemWithMeasuresABC(ABC):

    def __gt__(self, other):
        if not isinstance(other, datetime):
            raise TypeError(f"{type(self).__name__} in __gt__(): expected 'datetime' object, got {type(other).__name__}")
        return (self.measured_at_datetime() - other).total_seconds() > 0

    @abstractmethod
    def measured_at(self) -> str:
        pass

    @abstractmethod
    def measured_at_datetime(self) -> datetime:
        pass

    @abstractmethod
    def values(self) -> Set[Tuple[str, Any]]:
        pass

    def __repr__(self):
        return f"{type(self).__name__}(created_at={self.measured_at()}, values={self.values()!r})"


###################################### AtmotubeItem(object) ######################################
class AtmotubeItem(ItemWithMeasuresABC, ItemWithLocationABC):
    ATMOTUBE_MEASURE_PARAM = ['voc', 'pm1', 'pm25', 'pm10', 't', 'h', 'p']

    def __init__(self, item: Dict[str, Any]):
        self.item = item
        self._at = ""
        self._geom = ""
        self._at_datetime = None

    def measured_at_datetime(self) -> datetime:
        if self._at_datetime is None:
            self._at_datetime = datetime.strptime(self.measured_at(), SQL_DATETIME_FMT)
        return self._at_datetime

    def measured_at(self) -> str:
        if not self._at:
            self._at = self.item['time'].replace("T", " ").split('.')[0]
        return self._at

    def values(self) -> Set[Tuple[str, Any]]:
        return {(pcode, self.item.get(pcode)) for pcode in self.ATMOTUBE_MEASURE_PARAM}

    def located_at(self):
        if not self._geom:
            tmp = self.item.pop('coords', None)
            self._geom = "NULL"
            if tmp is not None:
                pt = POSTGIS_POINT.format(lat=tmp['lat'], lon=tmp['lon'])
                self._geom = ST_GEOM_FROM_TEXT.format(geom=pt, srid=26918)
        return self._geom

    def __repr__(self):
        return super().__repr__()


###################################### PurpleairItem(object) ######################################
class PurpleairItem(ItemWithIdentityABC, ItemWithLocationABC):
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

    def name(self) -> str:
        if not self._name:
            self._name = f"{self.item['name']} ({self.item['sensor_index']})"
        return self._name

    def type(self) -> str:
        return "Purpleair/Thingspeak"

    def channel_properties(self) -> Set[ChannelProperties]:
        if not self._channels:
            self._channels = {ChannelProperties(key=self.item[p['key']], ident=self.item[p['ident']], name=p['name'])
                              for p in self.CHANNELS_PARAM}
        return self._channels

    def created_at(self) -> str:
        if not self._at:
            self._at = datetime.fromtimestamp(self.item['date_created']).strftime(SQL_DATETIME_FMT)
        return self._at

    def located_at(self) -> str:
        if not self._geom:
            point = POSTGIS_POINT.format(lon=self.item['longitude'], lat=self.item['latitude'])
            self._geom = ST_GEOM_FROM_TEXT.format(geom=point, srid=26918)
        return self._geom


###################################### ThingspeakItem(object) ######################################
class ThingspeakItem(ItemWithMeasuresABC):

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
