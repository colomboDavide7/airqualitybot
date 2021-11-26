######################################################
#
# Author: Davide Colombo
# Date: 26/11/21 08:51
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import List, Dict, Any
import airquality.api.resp.resp as resp


class APIRespBuilder(abc.ABC):

    def __init__(self, api_resp_cls=resp.APIRESPTYPE):
        self.api_resp_cls = api_resp_cls

    @abc.abstractmethod
    def build(self, parsed_resp: Dict[str, Any]) -> List[resp.APIRESPTYPE]:
        pass


################################ ATMOTUBE RESPONSE BUILDER ################################
class AtmoAPIRespBuilder(APIRespBuilder):

    def __init__(self, api_resp_cls=resp.AtmoAPIResp):
        super(AtmoAPIRespBuilder, self).__init__(api_resp_cls=api_resp_cls)

    def build(self, parsed_resp: Dict[str, Any]) -> List[resp.AtmoAPIResp]:
        responses = []
        try:
            for item in parsed_resp['data']['items']:
                responses.append(self.api_resp_cls(item))
        except KeyError as ke:
            raise SystemExit(f"{AtmoAPIRespBuilder.__name__}: bad API response => missing key={ke!s}")
        return responses


################################ PURPLEAIR RESPONSE BUILDER ################################
class PurpAPIRespBuilder(APIRespBuilder):

    def __init__(self, api_resp_cls=resp.PurpAPIResp):
        super(PurpAPIRespBuilder, self).__init__(api_resp_cls=api_resp_cls)

    def build(self, parsed_resp: Dict[str, Any]) -> List[resp.PurpAPIResp]:
        responses = []
        try:
            for data_packet in parsed_resp['data']:
                responses.append(self.api_resp_cls(dict(zip(parsed_resp['fields'], data_packet))))
        except KeyError as ke:
            raise SystemExit(f"{PurpAPIRespBuilder.__name__}: bad API response => missing key={ke!s}")
        return responses


################################ THINGSPEAK RESPONSE BUILDER ################################
class ThnkRespBuilder(APIRespBuilder):

    def __init__(self, api_resp_cls=resp.THNKRESPTYPE):
        super(ThnkRespBuilder, self).__init__(api_resp_cls=api_resp_cls)

    def build(self, parsed_resp: Dict[str, Any]) -> List[resp.THNKRESPTYPE]:
        responses = []
        try:
            for feed in parsed_resp['feeds']:
                data = {'created_at': feed['created_at']}
                for field in self.api_resp_cls.FIELD_MAP:
                    field_name = self.api_resp_cls.FIELD_MAP[field]
                    field_value = feed[field]
                    data[field_name] = field_value
                responses.append(self.api_resp_cls(data))
        except KeyError as ke:
            raise SystemExit(f"{ThnkRespBuilder.__name__}: bad API response => missing key={ke!s}")
        return responses
