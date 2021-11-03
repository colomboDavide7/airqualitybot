######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 02/11/21 16:59
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from abc import ABC
from typing import Dict, Any
from airquality.parser.datetime_parser import DatetimeParser


DEFAULT_VALUE = 'null'


class PlainAPIPacket(ABC):
    pass


class PlainAPIPacketPurpleair(PlainAPIPacket):

    def __init__(self, api_param: Dict[str, Any]):
        self.name = api_param.get('name', DEFAULT_VALUE)
        self.sensor_index = api_param.get('sensor_index', DEFAULT_VALUE)
        self.latitude = api_param.get('latitude', DEFAULT_VALUE)
        self.longitude = api_param.get('longitude', DEFAULT_VALUE)
        self.primary_id_a = api_param.get('primary_id_a', DEFAULT_VALUE)
        self.primary_key_a = api_param.get('primary_key_a', DEFAULT_VALUE)
        self.primary_id_b = api_param.get('primary_id_b', DEFAULT_VALUE)
        self.primary_key_b = api_param.get('primary_key_b', DEFAULT_VALUE)
        self.secondary_id_a = api_param.get('secondary_id_a', DEFAULT_VALUE)
        self.secondary_key_a = api_param.get('secondary_key_a', DEFAULT_VALUE)
        self.secondary_id_b = api_param.get('secondary_id_b', DEFAULT_VALUE)
        self.secondary_key_b = api_param.get('secondary_key_b', DEFAULT_VALUE)
        self.purpleair_identifier = f"{self.name} ({self.sensor_index})"

    def __str__(self):
        return f"name={self.name}, sensor_index={self.sensor_index}, identifier={self.purpleair_identifier}, " \
               f"latitude={self.latitude}, longitude={self.longitude}, " \
               f"primary_id_a={self.primary_id_a}, primary_key_a={self.primary_key_a}, " \
               f"primary_id_b={self.primary_id_b}, primary_key_b={self.primary_key_b}, " \
               f"secondary_id_a={self.secondary_id_a}, secondary_key_a={self.secondary_key_a}, " \
               f"secondary_id_b={self.secondary_id_b}, secondary_key_b={self.secondary_key_b}"

    def __eq__(self, other):
        if not isinstance(other, PlainAPIPacketPurpleair):
            raise SystemExit(f"{PlainAPIPacketPurpleair.__name__}: cannot compare objects of different type.")
        return other.purpleair_identifier == self.purpleair_identifier


################################ ATMOTUBE PLAIN API PACKET ################################

class PlainAPIPacketAtmotube(PlainAPIPacket):

    def __init__(self, api_param: Dict[str, Any]):
        self.time = api_param.get('time', DEFAULT_VALUE)
        if self.time != DEFAULT_VALUE:
            self.time = DatetimeParser.atmotube_to_sqltimestamp(ts=self.time)
        self.voc = api_param.get('voc', DEFAULT_VALUE)
        self.pm1 = api_param.get('pm1', DEFAULT_VALUE)
        self.pm25 = api_param.get('pm25', DEFAULT_VALUE)
        self.pm10 = api_param.get('pm10', DEFAULT_VALUE)
        self.temperature = api_param.get('t', DEFAULT_VALUE)
        self.humidity = api_param.get('h', DEFAULT_VALUE)
        self.pressure = api_param.get('p', DEFAULT_VALUE)

    def __str__(self):
        return f"time={self.time}, voc={self.voc}, pm1.0={self.pm1}, pm2.5={self.pm25}, pm10.0={self.pm10}, " \
               f"temperature={self.temperature}, humidity={self.humidity}, pressure={self.pressure}"

    def __eq__(self, other):
        if not isinstance(other, PlainAPIPacketAtmotube):
            raise SystemExit(f"{PlainAPIPacketAtmotube.__name__}: cannot compare objects of different type.")
        return other.time == self.time and other.voc == self.voc and other.pm1 == self.pm1 and \
            other.pm25 == self.pm25 and other.pm10 == self.pm10 and other.temperature == self.temperature and \
            other.humidity == self.humidity and other.pressure == self.pressure
