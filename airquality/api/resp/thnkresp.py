######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 16:11
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any, List, Union
import airquality.api.resp.resp as resp


################################ THINGSPEAK API RESPONSE ################################
class ThnkCH1AResp(resp.APIResp):
    FIELD_MAP = {"field1": "pm1.0_atm_a", "field2": "pm2.5_atm_a", "field3": "pm10.0_atm_a", "field6": "temperature_a",
                 "field7": "humidity_a"}

    FIELDS = ["pm1.0_atm_a", "pm2.5_atm_a", "pm10.0_atm_a", "temperature_a", "humidity_a"]

    def __init__(self, data: Dict[str, Any]):
        try:
            self.created_at = data['created_at']
            self.measures = [resp.ParamNameValue(name=n, value=data.get(n)) for n in ThnkCH1AResp.FIELDS]
        except KeyError as ke:
            raise SystemExit(f"{ThnkCH1AResp.__name__}: bad API response => missing key='{ke!s}'")


class ThnkCH1BResp(resp.APIResp):
    FIELD_MAP = {"field1": "pm1.0_atm_b", "field2": "pm2.5_atm_b", "field3": "pm10.0_atm_b", "field6": "pressure_b"}

    FIELDS = ["pm1.0_atm_b", "pm2.5_atm_b", "pm10.0_atm_b", "pressure_b"]

    def __init__(self, data: Dict[str, Any]):
        try:
            self.created_at = data['created_at']
            self.measures = [resp.ParamNameValue(name=n, value=data.get(n)) for n in
                             ThnkCH1BResp.FIELDS]
        except KeyError as ke:
            raise SystemExit(f"{ThnkCH1BResp.__name__}: bad API response => missing key='{ke!s}'")


class ThnkCH2AResp(resp.APIResp):
    FIELD_MAP = {"field1": "0.3_um_count_a", "field2": "0.5_um_count_a", "field3": "1.0_um_count_a",
                 "field4": "2.5_um_count_a", "field5": "5.0_um_count_a", "field6": "10.0_um_count_a"}

    FIELDS = ["0.3_um_count_a", "0.5_um_count_a", "1.0_um_count_a",
              "2.5_um_count_a", "5.0_um_count_a", "10.0_um_count_a"]

    def __init__(self, data: Dict[str, Any]):
        try:
            self.created_at = data['created_at']
            self.measures = [resp.ParamNameValue(name=n, value=data.get(n)) for n in ThnkCH2AResp.FIELDS]
        except KeyError as ke:
            raise SystemExit(f"{ThnkCH2AResp.__name__}: bad API response => missing key='{ke!s}'")


class ThnkCH2BResp(resp.APIResp):
    FIELD_MAP = {"field1": "0.3_um_count_b", "field2": "0.5_um_count_b", "field3": "1.0_um_count_b",
                 "field4": "2.5_um_count_b", "field5": "5.0_um_count_b", "field6": "10.0_um_count_b"}

    FIELDS = ["0.3_um_count_b", "0.5_um_count_b", "1.0_um_count_b",
              "2.5_um_count_b", "5.0_um_count_b", "10.0_um_count_b"]

    def __init__(self, data: Dict[str, Any]):
        try:
            self.created_at = data['created_at']
            self.measures = [resp.ParamNameValue(name=n, value=data.get(n)) for n in ThnkCH2BResp.FIELDS]
        except KeyError as ke:
            raise SystemExit(f"{ThnkCH2BResp.__name__}: bad API response => missing key='{ke!s}'")


################################ THINGSPEAK RESPONSE BUILDER ################################
RESP_TYPE = Union[ThnkCH1AResp, ThnkCH1BResp, ThnkCH2AResp, ThnkCH2BResp]


class ThnkRespBuilder(resp.APIRespBuilder):

    def __init__(self, api_resp_cls=RESP_TYPE):
        super(ThnkRespBuilder, self).__init__(api_resp_cls=api_resp_cls)

    def build(self, parsed_resp: Dict[str, Any]) -> List[RESP_TYPE]:
        responses = []
        try:
            for feed in parsed_resp['feeds']:
                data = {'created_at': feed['created_at']}
                for field in self.api_response_class.FIELD_MAP:
                    field_name = self.api_response_class.FIELD_MAP[field]
                    field_value = feed[field]
                    data[field_name] = field_value
                responses.append(self.api_response_class(data))
        except KeyError as ke:
            raise SystemExit(f"{ThnkRespBuilder.__name__}: bad API response => missing key={ke!s}")
        return responses
