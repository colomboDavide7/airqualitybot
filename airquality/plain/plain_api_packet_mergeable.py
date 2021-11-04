######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 04/11/21 10:14
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any
from abc import ABC, abstractmethod
from airquality.constants.shared_constants import PARAM_DEFAULT_VALUE
from airquality.parser.datetime_parser import DatetimeParser


class PlainAPIPacketMergeable(ABC):

    def __init__(self, created_at: str):
        self.created_at = DatetimeParser.thingspeak_to_sqltimestamp(created_at)

    @abstractmethod
    def plain2dict(self) -> Dict[str, Any]:
        pass


################################ THINGSPEAK PLAIN API PACKET FOR PRIMARY CHANNEL A ################################

class PlainAPIPacketThingspeakPrimaryChannelA(PlainAPIPacketMergeable):

    def __init__(self, api_answer: Dict[str, Any]):
        super().__init__(created_at=api_answer.get('created_at'))
        self.pm1 = api_answer.get('pm1.0_atm_a', PARAM_DEFAULT_VALUE)
        self.pm25 = api_answer.get('pm2.5_atm_a', PARAM_DEFAULT_VALUE)
        self.pm10 = api_answer.get('pm10.0_atm_a', PARAM_DEFAULT_VALUE)
        self.temperature = api_answer.get('temperature_a', PARAM_DEFAULT_VALUE)
        self.humidity = api_answer.get('humidity_a', PARAM_DEFAULT_VALUE)

    def __str__(self):
        return f"timestamp={self.created_at}, pm1.0_atm_a={self.pm1}, pm2.5_atm_a={self.pm25}, pm10.0_atm_a={self.pm10}, " \
               f"temperature_a={self.temperature}, humidity_a={self.humidity}"

    def plain2dict(self) -> Dict[str, Any]:
        return {'pm1a': self.pm1, 'pm25a': self.pm25, 'pm10a': self.pm10, 'temperature': self.temperature,
                'humidity': self.humidity}


class PlainAPIPacketThingspeakPrimaryChannelB(PlainAPIPacketMergeable):

    def __init__(self, api_answer: Dict[str, Any]):
        super().__init__(created_at=api_answer.get('created_at'))
        self.pm1 = api_answer.get('pm1.0_atm_b', PARAM_DEFAULT_VALUE)
        self.pm25 = api_answer.get('pm2.5_atm_b', PARAM_DEFAULT_VALUE)
        self.pm10 = api_answer.get('pm10.0_atm_b', PARAM_DEFAULT_VALUE)
        self.pressure = api_answer.get('pressure_b', PARAM_DEFAULT_VALUE)

    def __str__(self):
        return f"timestamp={self.created_at}, pm1.0_atm_b={self.pm1}, pm2.5_atm_b={self.pm25}, pm10.0_atm_b={self.pm10}, " \
               f"pressure_b={self.pressure}"

    def plain2dict(self) -> Dict[str, Any]:
        return {'pm1b': self.pm1, 'pm25b': self.pm25, 'pm10b': self.pm10, 'pressure': self.pressure}


class PlainAPIPacketThingspeakSecondaryChannelA(PlainAPIPacketMergeable):

    def __init__(self, api_answer: Dict[str, Any]):
        super().__init__(created_at=api_answer.get('created_at'))
        self.count_03 = api_answer.get('0.3_um_count_a', PARAM_DEFAULT_VALUE)
        self.count_05 = api_answer.get('0.5_um_count_a', PARAM_DEFAULT_VALUE)
        self.count_1 = api_answer.get('1.0_um_count_a', PARAM_DEFAULT_VALUE)
        self.count_25 = api_answer.get('2.5_um_count_a', PARAM_DEFAULT_VALUE)
        self.count_5 = api_answer.get('5.0_um_count_a', PARAM_DEFAULT_VALUE)
        self.count_10 = api_answer.get('10.0_um_count_a', PARAM_DEFAULT_VALUE)

    def __str__(self):
        return f"timestamp={self.created_at}, 0.3_um_count_a={self.count_03}, 0.5_um_count_a={self.count_05}, 1.0_um_count_a={self.count_1}, " \
               f"2.5_um_count_a={self.count_25}, 5.0_um_count_a={self.count_5}, 10.0_um_count_a={self.count_10}"

    def plain2dict(self) -> Dict[str, Any]:
        return {'count03a': self.count_03, 'count05a': self.count_05, 'count1a': self.count_1,
                'count25a': self.count_25, 'count5a': self.count_5, 'count10a': self.count_10}


class PlainAPIPacketThingspeakSecondaryChannelB(PlainAPIPacketMergeable):

    def __init__(self, api_answer: Dict[str, Any]):
        super().__init__(created_at=api_answer.get('created_at'))
        self.count_03 = api_answer.get('0.3_um_count_b', PARAM_DEFAULT_VALUE)
        self.count_05 = api_answer.get('0.5_um_count_b', PARAM_DEFAULT_VALUE)
        self.count_1 = api_answer.get('1.0_um_count_b', PARAM_DEFAULT_VALUE)
        self.count_25 = api_answer.get('2.5_um_count_b', PARAM_DEFAULT_VALUE)
        self.count_5 = api_answer.get('5.0_um_count_b', PARAM_DEFAULT_VALUE)
        self.count_10 = api_answer.get('10.0_um_count_b', PARAM_DEFAULT_VALUE)

    def __str__(self):
        return f"timestamp={self.created_at}, 0.3_um_count_b={self.count_03}, 0.5_um_count_b={self.count_05}, 1.0_um_count_b={self.count_1}, " \
               f"2.5_um_count_b={self.count_25}, 5.0_um_count_b={self.count_5}, 10.0_um_count_b={self.count_10}"

    def plain2dict(self) -> Dict[str, Any]:
        return {'count03b': self.count_03, 'count05b': self.count_05, 'count1b': self.count_1,
                'count25b': self.count_25, 'count5b': self.count_5, 'count10b': self.count_10}


################################ THINGSPEAK PLAIN API PACKET FACTORY ################################
class PlainAPIPacketThingspeakFactory(ABC):

    @abstractmethod
    def make_plain_object(self, api_answer: Dict[str, Any]) -> PlainAPIPacketMergeable:
        pass


class PlainAPIPacketThingspeakPrimaryChannelAFactory(PlainAPIPacketThingspeakFactory):

    def make_plain_object(self, api_answer: Dict[str, Any]) -> PlainAPIPacketThingspeakPrimaryChannelA:
        return PlainAPIPacketThingspeakPrimaryChannelA(api_answer)


class PlainAPIPacketThingspeakPrimaryChannelBFactory(PlainAPIPacketThingspeakFactory):

    def make_plain_object(self, api_answer: Dict[str, Any]) -> PlainAPIPacketThingspeakPrimaryChannelB:
        return PlainAPIPacketThingspeakPrimaryChannelB(api_answer)


class PlainAPIPacketThingspeakSecondaryChannelAFactory(PlainAPIPacketThingspeakFactory):

    def make_plain_object(self, api_answer: Dict[str, Any]) -> PlainAPIPacketThingspeakSecondaryChannelA:
        return PlainAPIPacketThingspeakSecondaryChannelA(api_answer)


class PlainAPIPacketThingspeakSecondaryChannelBFactory(PlainAPIPacketThingspeakFactory):

    def make_plain_object(self, api_answer: Dict[str, Any]) -> PlainAPIPacketThingspeakSecondaryChannelB:
        return PlainAPIPacketThingspeakSecondaryChannelB(api_answer)
