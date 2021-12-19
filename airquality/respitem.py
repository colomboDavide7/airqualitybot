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


from typing import Dict, Any
from datetime import datetime


class AtmotubeItem(object):
    ATMOTUBE_MEASURE_PARAM = ['voc', 'pm1', 'pm25', 'pm10', 't', 'h', 'p']

    def __init__(self, item: Dict[str, Any]):
        self.item = item
        self._at = ""
        self._coords = ""
        self._at_datetime = ""

    def __gt__(self, other):
        if not isinstance(other, datetime):
            raise TypeError(f"{type(self).__name__} expected 'datetime' object, got {type(other).__name__}")
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
    def values(self):
        return [(pcode, self.item.get(pcode)) for pcode in self.ATMOTUBE_MEASURE_PARAM]
