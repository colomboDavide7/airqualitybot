######################################################
#
# Author: Davide Colombo
# Date: 28/12/21 12:22
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict
from datetime import datetime
from airquality.respitem import PurpleairItem, AtmotubeItem

SQL_DATETIME_FMT = "%Y-%m-%d %H:%M:%S"
ST_GEOM_FROM_TEXT = "ST_GeomFromText('{geom}', {srid})"
POSTGIS_POINT = "POINT({lon} {lat})"


###################################### PurpleairSQLItem(object) ######################################s
class PurpleairSQLItem(object):

    SENSOR_RECORD_TEMPLATE = "({sensor_id}, '%s', '%s'),"
    APIPARAM_RECORD_TEMPLATE = "({sensor_id}, '%s', '%s', '%s', '%s')"
    LOCATION_RECORD_TEMPLATE = "({sensor_id}, '%s', %s),"

    def __init__(self, item: PurpleairItem):
        self.item = item

    @property
    def sensor(self) -> str:
        return self.SENSOR_RECORD_TEMPLATE % ('Purpleair/Thingspeak', self.item.name)

    @property
    def apiparam(self) -> str:
        last_activity = datetime.fromtimestamp(self.item.date_created).strftime(SQL_DATETIME_FMT)
        return ','.join(self.APIPARAM_RECORD_TEMPLATE % (c.key, c.ident, c.name, last_activity)
                        for c in self.item.channels) + ','

    @property
    def sensor_location(self) -> str:
        now = datetime.now().strftime(SQL_DATETIME_FMT)
        point = POSTGIS_POINT.format(lon=self.item.longitude, lat=self.item.latitude)
        location = ST_GEOM_FROM_TEXT.format(geom=point, srid=26918)
        return self.LOCATION_RECORD_TEMPLATE % (now, location)


class AtmotubeSQLItem(object):

    MEASURE_TEMPLATE = "({packet_id}, %s, '%s', '%s', %s),"

    def __init__(self, item: AtmotubeItem, measure_param: Dict[str, int]):
        self.item = item
        self.measure_param = measure_param

    @property
    def measured_at(self) -> str:
        return self.item.time.replace("T", " ").split('.')[0]

    @property
    def measurement(self) -> str:
        measured_at = self.measured_at
        geom = self._get_geom()
        return ','.join(
            self.MEASURE_TEMPLATE % (self.measure_param[param_code], param_value, measured_at, geom)
            for param_code, param_value in self.item.values) + ','

    def _get_geom(self) -> str:
        coords = self.item.coords
        if coords is None:
            return "NULL"
        point = POSTGIS_POINT.format(lon=coords['lon'], lat=coords['lat'])
        return ST_GEOM_FROM_TEXT.format(geom=point, srid=26918)
