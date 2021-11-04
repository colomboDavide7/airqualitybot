######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 04/11/21 12:51
# Description: INSERT HERE THE DESCRIPTION
#
######################################################

from abc import ABC, abstractmethod
from typing import Dict, Any


class PlainExtensibleAPIPacket(ABC):

    @abstractmethod
    def extend(self, api_answer: Dict[str, Any]) -> None:
        pass


class PlainExtensibleAPIPacketThingspeak(PlainExtensibleAPIPacket):

    def __init__(self):
        self.pm1a = self.pm25a = self.pm10a = self.temperature = self.humidity = None
        self.pm1b = self.pm25b = self.pm10b = self.pressure = None
        self.count_03a = self.count_05a = self.count_1a = self.count_25a = self.count_5a = self.count_10a = None
        self.count_03b = self.count_05b = self.count_1b = self.count_25b = self.count_5b = self.count_10b = None

    def __try_to_extend_param_primary_channel_a_param(self, api_answer: Dict[str, Any]) -> None:
        if self.pm1a is None:
            self.pm1a = api_answer.get('pm1.0_atm_a')
        if self.pm25a is None:
            self.pm25a = api_answer.get('pm2.5_atm_a')
        if self.pm10a is None:
            self.pm10a = api_answer.get('pm10.0_atm_a')
        if self.temperature is None:
            self.temperature = api_answer.get('temperature_a')
        if self.humidity is None:
            self.humidity = api_answer.get('humidity_a')

    def __try_to_extend_param_primary_channel_b_param(self, api_answer: Dict[str, Any]) -> None:
        if self.pm1b is None:
            self.pm1b = api_answer.get('pm1.0_atm_b')
        if self.pm25b is None:
            self.pm25b = api_answer.get('pm2.5_atm_b')
        if self.pm10b is None:
            self.pm10b = api_answer.get('pm10.0_atm_b')
        if self.pressure is None:
            self.pressure = api_answer.get('pressure_b')

    def __try_to_extend_param_secondary_channel_a_param(self, api_answer: Dict[str, Any]) -> None:
        if self.count_03a is None:
            self.count_03a = api_answer.get('0.3_um_count_a')
        if self.count_05a is None:
            self.count_05a = api_answer.get('0.5_um_count_a')
        if self.count_1a is None:
            self.count_1a = api_answer.get('1.0_um_count_a')
        if self.count_25a is None:
            self.count_25a = api_answer.get('2.5_um_count_a')
        if self.count_5a is None:
            self.count_5a = api_answer.get('5.0_um_count_a')
        if self.count_10a is None:
            self.count_10a = api_answer.get('10.0_um_count_a')

    def __try_to_extend_param_secondary_channel_b_param(self, api_answer: Dict[str, Any]) -> None:
        if self.count_03a is None:
            self.count_03a = api_answer.get('0.3_um_count_b')
        if self.count_05a is None:
            self.count_05a = api_answer.get('0.5_um_count_b')
        if self.count_1a is None:
            self.count_1a = api_answer.get('1.0_um_count_b')
        if self.count_25a is None:
            self.count_25a = api_answer.get('2.5_um_count_b')
        if self.count_5a is None:
            self.count_5a = api_answer.get('5.0_um_count_b')
        if self.count_10a is None:
            self.count_10a = api_answer.get('10.0_um_count_b')

    def extend(self, api_answer: Dict[str, Any]) -> None:

        if self.pm1a is None and self.pm25a is None and self.pm10a is None and self.temperature is None and self.humidity is None:
            self.__try_to_extend_param_primary_channel_a_param(api_answer)

        if self.pm1b is None and self.pm25b is None and self.pm10b is None and self.pressure is None:
            self.__try_to_extend_param_primary_channel_b_param(api_answer)

        if self.count_03a is None and self.count_05a is None and self.count_1a is None and self.count_25a is None and \
           self.count_5a is None and self.count_10a is None:
            self.__try_to_extend_param_secondary_channel_a_param(api_answer)

        if self.count_03b is None and self.count_05b is None and self.count_1b is None and self.count_25b is None and \
           self.count_5b is None and self.count_10b is None:
            self.__try_to_extend_param_secondary_channel_a_param(api_answer)
