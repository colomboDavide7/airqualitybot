######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 16:11
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any, List, Union


################################ THINGSPEAK API RESPONSE MODEL ################################
class ThingspeakChannel1AResponseModel:
    FIELD_MAP = {"field1": "pm1.0_atm_a", "field2": "pm2.5_atm_a", "field3": "pm10.0_atm_a", "field6": "temperature_a",
                 "field7": "humidity_a"}

    def __init__(self, data: Dict[str, Any]):
        try:
            self.created_at = data['created_at']
            self.pm1 = data['pm1.0_atm_a']
            self.pm25 = data['pm2.5_atm_a']
            self.pm10 = data['pm10.0_atm_a']
            self.temp = data['temperature_a']
            self.hum = data['humidity_a']
        except KeyError as ke:
            raise SystemExit(f"{ThingspeakChannel1AResponseModel.__name__}: bad sensor data => missing key='{ke!s}'")


class ThingspeakChannel1BResponseModel:
    FIELD_MAP = {"field1": "pm1.0_atm_b", "field2": "pm2.5_atm_b", "field3": "pm10.0_atm_b", "field6": "pressure_b"}

    def __init__(self, data: Dict[str, Any]):
        try:
            self.created_at = data['created_at']
            self.pm1 = data['pm1.0_atm_b']
            self.pm25 = data['pm2.5_atm_b']
            self.pm10 = data['pm10.0_atm_b']
            self.press = data['pressure_b']
        except KeyError as ke:
            raise SystemExit(f"{ThingspeakChannel1BResponseModel.__name__}: bad sensor data => missing key='{ke!s}'")


class ThingspeakChannel2AResponseModel:
    FIELD_MAP = {"field1": "0.3_um_count_a", "field2": "0.5_um_count_a", "field3": "1.0_um_count_a",
                 "field4": "2.5_um_count_a", "field5": "5.0_um_count_a", "field6": "10.0_um_count_a"}

    def __init__(self, data: Dict[str, Any]):
        try:
            self.created_at = data['created_at']
            self.count_03 = data['0.3_um_count_a']
            self.count_05 = data['0.5_um_count_a']
            self.count_1 = data['1.0_um_count_a']
            self.count_25 = data['2.5_um_count_a']
            self.count_5 = data['5.0_um_count_a']
            self.count_10 = data['10.0_um_count_a']
        except KeyError as ke:
            raise SystemExit(f"{ThingspeakChannel2AResponseModel.__name__}: bad sensor data => missing key='{ke!s}'")


class ThingspeakChannel2BResponseModel:
    FIELD_MAP = {"field1": "0.3_um_count_b", "field2": "0.5_um_count_b", "field3": "1.0_um_count_b",
                 "field4": "2.5_um_count_b", "field5": "5.0_um_count_b", "field6": "10.0_um_count_b"}

    def __init__(self, data: Dict[str, Any]):
        try:
            self.created_at = data['created_at']
            self.count_03 = data['0.3_um_count_b']
            self.count_05 = data['0.5_um_count_b']
            self.count_1 = data['1.0_um_count_b']
            self.count_25 = data['2.5_um_count_b']
            self.count_5 = data['5.0_um_count_b']
            self.count_10 = data['10.0_um_count_b']
        except KeyError as ke:
            raise SystemExit(f"{ThingspeakChannel2BResponseModel.__name__}: bad sensor data => missing key='{ke!s}'")


RESP_MODEL_TYPE = Union[
    ThingspeakChannel1AResponseModel,
    ThingspeakChannel1BResponseModel,
    ThingspeakChannel2AResponseModel,
    ThingspeakChannel2BResponseModel]


################################ THINGSPEAK RESPONSE MODEL BUILDER CLASS ################################
class ThingspeakAPIResponseModelBuilder:

    def __init__(self, response_model_class=RESP_MODEL_TYPE):
        self.response_model_class = response_model_class

    def get_responses(self, parsed_response: Dict[str, Any]) -> List[RESP_MODEL_TYPE]:
        responses = []
        try:
            for feed in parsed_response['feeds']:
                data = {'created_at': feed['created_at']}
                for field in self.response_model_class.FIELD_MAP:
                    field_name = self.response_model_class.FIELD_MAP[field]
                    field_value = feed[field]
                    data[field_name] = field_value
                responses.append(self.response_model_class(data))
        except KeyError as ke:
            raise SystemExit(f"{ThingspeakAPIResponseModelBuilder.__name__}: bas sensor data => missing key={ke!s}")
        return responses
