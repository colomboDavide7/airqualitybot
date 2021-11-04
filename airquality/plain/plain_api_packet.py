######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 02/11/21 16:59
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import builtins
from abc import ABC
from typing import Dict, Any
from airquality.parser.datetime_parser import DatetimeParser
from airquality.constants.shared_constants import PARAM_DEFAULT_VALUE


class PlainAPIPacket(ABC):
    pass


class PlainAPIPacketPurpleair(builtins.object):

    def __init__(self, api_answer: Dict[str, Any]):
        self.name = api_answer.get('name', PARAM_DEFAULT_VALUE)
        self.sensor_index = api_answer.get('sensor_index', PARAM_DEFAULT_VALUE)
        self.latitude = api_answer.get('latitude', PARAM_DEFAULT_VALUE)
        self.longitude = api_answer.get('longitude', PARAM_DEFAULT_VALUE)
        self.primary_id_a = api_answer.get('primary_id_a', PARAM_DEFAULT_VALUE)
        self.primary_key_a = api_answer.get('primary_key_a', PARAM_DEFAULT_VALUE)
        self.primary_id_b = api_answer.get('primary_id_b', PARAM_DEFAULT_VALUE)
        self.primary_key_b = api_answer.get('primary_key_b', PARAM_DEFAULT_VALUE)
        self.secondary_id_a = api_answer.get('secondary_id_a', PARAM_DEFAULT_VALUE)
        self.secondary_key_a = api_answer.get('secondary_key_a', PARAM_DEFAULT_VALUE)
        self.secondary_id_b = api_answer.get('secondary_id_b', PARAM_DEFAULT_VALUE)
        self.secondary_key_b = api_answer.get('secondary_key_b', PARAM_DEFAULT_VALUE)
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

class PlainAPIPacketAtmotube(builtins.object):

    def __init__(self, api_answer: Dict[str, Any]):
        # handle timestamp
        self.time = api_answer.get('time', PARAM_DEFAULT_VALUE)
        if self.time != PARAM_DEFAULT_VALUE:
            self.time = DatetimeParser.atmotube_to_sqltimestamp(ts=self.time)

        # handle geolocation (if any)
        self.latitude = PARAM_DEFAULT_VALUE
        self.longitude = PARAM_DEFAULT_VALUE
        if api_answer.get('coords', PARAM_DEFAULT_VALUE) != PARAM_DEFAULT_VALUE:
            self.latitude = api_answer['coords']['lat']
            self.longitude = api_answer['coords']['lon']

        self.voc = api_answer.get('voc', PARAM_DEFAULT_VALUE)
        self.pm1 = api_answer.get('pm1', PARAM_DEFAULT_VALUE)
        self.pm25 = api_answer.get('pm25', PARAM_DEFAULT_VALUE)
        self.pm10 = api_answer.get('pm10', PARAM_DEFAULT_VALUE)
        self.temperature = api_answer.get('t', PARAM_DEFAULT_VALUE)
        self.humidity = api_answer.get('h', PARAM_DEFAULT_VALUE)
        self.pressure = api_answer.get('p', PARAM_DEFAULT_VALUE)

    def __str__(self):
        return f"time={self.time}, voc={self.voc}, pm1.0={self.pm1}, pm2.5={self.pm25}, pm10.0={self.pm10}, " \
               f"temperature={self.temperature}, humidity={self.humidity}, pressure={self.pressure}, " \
               f"latitude={self.latitude}, longitude={self.longitude}"

    def __eq__(self, other):
        if not isinstance(other, PlainAPIPacketAtmotube):
            raise SystemExit(f"{PlainAPIPacketAtmotube.__name__}: cannot compare objects of different type.")
        return other.time == self.time and other.voc == self.voc and other.pm1 == self.pm1 and \
            other.pm25 == self.pm25 and other.pm10 == self.pm10 and other.temperature == self.temperature and \
            other.humidity == self.humidity and other.pressure == self.pressure
