#################################################
#
# @Author: davidecolombo
# @Date: mer, 27-10-2021, 10:24
# @Description: this script defines the classes for formatting API address for fetching data from API
#
#################################################
import builtins
from abc import ABC, abstractmethod
from typing import Dict, Any
from airquality.constants.shared_constants import PURPLEAIR_CH_ID_PARAM


class APIAddressFormatter(ABC):


    def __init__(self):
        self.__raw_address = None


    @property
    def raw_address(self):
        return self.__raw_address


    @raw_address.setter
    def raw_address(self, value: str):
        self.__raw_address = value


    @abstractmethod
    def format_address(self, fmt: Dict[str, Any]) -> str:
        pass


class DefaultAPIAddressFormatter(APIAddressFormatter):


    def format_address(self, fmt: Dict[str, Any] = None) -> str:

        if self.raw_address is None:
            raise SystemExit(f"{APIAddressFormatterPurpleair.__name__}: cannot format 'None' API address.")
        return self.raw_address



class APIAddressFormatterPurpleair(APIAddressFormatter):


    def __init__(self):
        super().__init__()
        self.__formatted_address = ""


    def format_address(self, fmt: Dict[str, Any]) -> str:

        if self.raw_address is None:
            raise SystemExit(f"{APIAddressFormatterPurpleair.__name__}: cannot format 'None' API address.")

        if PURPLEAIR_CH_ID_PARAM not in fmt.keys():
            raise SystemExit(f"{APIAddressFormatterPurpleair.__name__}: missing '{PURPLEAIR_CH_ID_PARAM}' key.")

        self.__formatted_address = self.raw_address.format(channel_id = fmt[PURPLEAIR_CH_ID_PARAM])
        return self.__formatted_address



################################ FACTORY ################################
class APIAddressFormatterFactory(builtins.object):


    @classmethod
    def create_api_address_formatter(cls, bot_personality: str) -> APIAddressFormatter:

        if bot_personality == "purpleair":
            return APIAddressFormatterPurpleair()
        elif bot_personality == "atmotube":
            """Return the default formatter because this functionality is not necessary for Atmotube sensors"""
            return DefaultAPIAddressFormatter()
        else:
            raise SystemExit(f"{APIAddressFormatterFactory.__name__}: cannot instantiate {APIAddressFormatter.__name__} "
                             f"instance for personality='{bot_personality}'.")
