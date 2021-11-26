######################################################
#
# Author: Davide Colombo
# Date: 25/11/21 18:46
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import Dict, Any
import airquality.api.url.baseurl as base


class DynamicURLBuilder(base.BaseURLBuilder, abc.ABC):

    def __init__(self, address: str, options: Dict[str, Any]):
        super(DynamicURLBuilder, self).__init__(address=address, options=options)
        self.api_key = None
        self.identifier = None

    def with_api_key(self, api_key: str):
        self.api_key = api_key
        return self

    def with_identifier(self, ident: str):
        self.identifier = ident
        return self


############################# ATMOTUBE URL BUILDER ##############################
class AtmotubeURLBuilder(DynamicURLBuilder):

    def __init__(self, address: str, options: Dict[str, Any]):
        super(AtmotubeURLBuilder, self).__init__(address=address, options=options)

    def build(self) -> str:
        return f"{self.address}?api_key={self.api_key}&mac={self.identifier}&{self._get_options_querystring()}"


############################# THINGSPEAK URL BUILDER ##############################
class ThingspeakURLBuilder(DynamicURLBuilder):

    def __init__(self, address: str, options: Dict[str, Any], fmt: str):
        super(ThingspeakURLBuilder, self).__init__(address=address, options=options)
        self.format = fmt

    def build(self) -> str:
        return f"{self.address}/{self.identifier}/feeds.{self.format}?api_key={self.api_key}&{self._get_options_querystring()}"
