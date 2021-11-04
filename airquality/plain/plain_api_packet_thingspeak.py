######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 04/11/21 10:14
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import builtins
from typing import Dict, Any
from abc import ABC, abstractmethod
from airquality.constants.shared_constants import PARAM_DEFAULT_VALUE


################################ THINGSPEAK PLAIN API PACKET FOR PRIMARY CHANNEL A ################################

class PlainAPIPacketThingspeakPrimaryChannelA(builtins.object):

    def __init__(self, api_answer: Dict[str, Any]):
        self.pm1 = api_answer.get('pm1.0_atm_a', PARAM_DEFAULT_VALUE)
        self.pm25 = api_answer.get('pm2.5_atm_a', PARAM_DEFAULT_VALUE)
        self.pm10 = api_answer.get('pm10.0_atm_a', PARAM_DEFAULT_VALUE)
        self.temperature = api_answer.get('temperature_a', PARAM_DEFAULT_VALUE)
        self.humidity = api_answer.get('humidity_a', PARAM_DEFAULT_VALUE)

    def __str__(self):
        return f"pm1.0_atm_a={self.pm1}, pm2.5_atm_a={self.pm25}, pm10.0_atm_a={self.pm10}, " \
               f"temperature_a={self.temperature}, humidity_a={self.humidity}"


class PlainAPIPacketThingspeakPrimaryChannelB(builtins.object):

    def __init__(self, api_answer: Dict[str, Any]):
        self.pm1 = api_answer.get('pm1.0_atm_b', PARAM_DEFAULT_VALUE)
        self.pm25 = api_answer.get('pm2.5_atm_b', PARAM_DEFAULT_VALUE)
        self.pm10 = api_answer.get('pm10.0_atm_b', PARAM_DEFAULT_VALUE)
        self.pressure = api_answer.get('pressure_b', PARAM_DEFAULT_VALUE)

    def __str__(self):
        return f"pm1.0_atm_b={self.pm1}, pm2.5_atm_b={self.pm25}, pm10.0_atm_b={self.pm10}, " \
               f"pressure_b={self.pressure}"


class PlainAPIPacketThingspeakSecondaryChannelA(builtins.object):

    def __init__(self, api_answer: Dict[str, Any]):
        self.count_03 = api_answer.get('0.3_um_count_a', PARAM_DEFAULT_VALUE)
        self.count_05 = api_answer.get('0.5_um_count_a', PARAM_DEFAULT_VALUE)
        self.count_1 = api_answer.get('1.0_um_count_a', PARAM_DEFAULT_VALUE)
        self.count_25 = api_answer.get('2.5_um_count_a', PARAM_DEFAULT_VALUE)
        self.count_5 = api_answer.get('5.0_um_count_a', PARAM_DEFAULT_VALUE)
        self.count_10 = api_answer.get('10.0_um_count_a', PARAM_DEFAULT_VALUE)

    def __str__(self):
        return f"0.3_um_count_a={self.count_03}, 0.5_um_count_a={self.count_05}, 1.0_um_count_a={self.count_1}, " \
               f"2.5_um_count_a={self.count_25}, 5.0_um_count_a={self.count_5}, 10.0_um_count_a={self.count_10}"


class PlainAPIPacketThingspeakSecondaryChannelB(builtins.object):

    def __init__(self, api_answer: Dict[str, Any]):
        self.count_03 = api_answer.get('0.3_um_count_b', PARAM_DEFAULT_VALUE)
        self.count_05 = api_answer.get('0.5_um_count_b', PARAM_DEFAULT_VALUE)
        self.count_1 = api_answer.get('1.0_um_count_b', PARAM_DEFAULT_VALUE)
        self.count_25 = api_answer.get('2.5_um_count_b', PARAM_DEFAULT_VALUE)
        self.count_5 = api_answer.get('5.0_um_count_b', PARAM_DEFAULT_VALUE)
        self.count_10 = api_answer.get('10.0_um_count_b', PARAM_DEFAULT_VALUE)

    def __str__(self):
        return f"0.3_um_count_b={self.count_03}, 0.5_um_count_b={self.count_05}, 1.0_um_count_b={self.count_1}, " \
               f"2.5_um_count_b={self.count_25}, 5.0_um_count_b={self.count_5}, 10.0_um_count_b={self.count_10}"


################################ THINGSPEAK PLAIN API PACKET FACTORY ################################
class PlainAPIPacketThingspeakFactory(ABC):

    @abstractmethod
    def make_plain_object(self, api_answer: Dict[str, Any]) -> builtins.object:
        pass


class PlainAPIPacketThingspeakPrimaryChannelAFactory(PlainAPIPacketThingspeakFactory):

    def make_plain_object(self, api_answer: Dict[str, Any]) -> PlainAPIPacketThingspeakPrimaryChannelA:
        return PlainAPIPacketThingspeakPrimaryChannelA(api_answer)


class PlainAPIPacketThingspeakPrimaryChannelBFactory(PlainAPIPacketThingspeakFactory):

    def make_plain_object(self, api_answer: Dict[str, Any]) -> builtins.object:
        return PlainAPIPacketThingspeakPrimaryChannelB(api_answer)


class PlainAPIPacketThingspeakSecondaryChannelAFactory(PlainAPIPacketThingspeakFactory):

    def make_plain_object(self, api_answer: Dict[str, Any]) -> builtins.object:
        return PlainAPIPacketThingspeakSecondaryChannelA(api_answer)


class PlainAPIPacketThingspeakSecondaryChannelBFactory(PlainAPIPacketThingspeakFactory):

    def make_plain_object(self, api_answer: Dict[str, Any]) -> builtins.object:
        return PlainAPIPacketThingspeakSecondaryChannelB(api_answer)
