######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 16:11
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any, List, Union
import airquality.api.model.baseresp as base


################################ THINGSPEAK API RESPONSE MODEL ################################
class ThingspeakChannel1AResponseModel(base.BaseResponseModel):
    FIELD_MAP = {"field1": "pm1.0_atm_a", "field2": "pm2.5_atm_a", "field3": "pm10.0_atm_a", "field6": "temperature_a",
                 "field7": "humidity_a"}

    FIELDS = ["pm1.0_atm_a", "pm2.5_atm_a", "pm10.0_atm_a", "temperature_a", "humidity_a"]

    def __init__(self, data: Dict[str, Any]):
        try:
            self.created_at = data['created_at']
            self.parameters = [base.ParamNameValue(name=n, value=data.get(n)) for n in ThingspeakChannel1AResponseModel.FIELDS]
        except KeyError as ke:
            raise SystemExit(f"{ThingspeakChannel1AResponseModel.__name__}: bad sensor data => missing key='{ke!s}'")


class ThingspeakChannel1BResponseModel(base.BaseResponseModel):
    FIELD_MAP = {"field1": "pm1.0_atm_b", "field2": "pm2.5_atm_b", "field3": "pm10.0_atm_b", "field6": "pressure_b"}

    FIELDS = ["pm1.0_atm_b", "pm2.5_atm_b", "pm10.0_atm_b", "pressure_b"]

    def __init__(self, data: Dict[str, Any]):
        try:
            self.created_at = data['created_at']
            self.parameters = [base.ParamNameValue(name=n, value=data.get(n)) for n in
                               ThingspeakChannel1BResponseModel.FIELDS]
        except KeyError as ke:
            raise SystemExit(f"{ThingspeakChannel1BResponseModel.__name__}: bad sensor data => missing key='{ke!s}'")


class ThingspeakChannel2AResponseModel(base.BaseResponseModel):
    FIELD_MAP = {"field1": "0.3_um_count_a", "field2": "0.5_um_count_a", "field3": "1.0_um_count_a",
                 "field4": "2.5_um_count_a", "field5": "5.0_um_count_a", "field6": "10.0_um_count_a"}

    FIELDS = ["0.3_um_count_a", "0.5_um_count_a", "1.0_um_count_a",
              "2.5_um_count_a", "5.0_um_count_a", "10.0_um_count_a"]

    def __init__(self, data: Dict[str, Any]):
        try:
            self.created_at = data['created_at']
            self.parameters = [base.ParamNameValue(name=n, value=data.get(n)) for n in ThingspeakChannel2AResponseModel.FIELDS]
        except KeyError as ke:
            raise SystemExit(f"{ThingspeakChannel2AResponseModel.__name__}: bad sensor data => missing key='{ke!s}'")


class ThingspeakChannel2BResponseModel(base.BaseResponseModel):
    FIELD_MAP = {"field1": "0.3_um_count_b", "field2": "0.5_um_count_b", "field3": "1.0_um_count_b",
                 "field4": "2.5_um_count_b", "field5": "5.0_um_count_b", "field6": "10.0_um_count_b"}

    FIELDS = ["0.3_um_count_b", "0.5_um_count_b", "1.0_um_count_b",
              "2.5_um_count_b", "5.0_um_count_b", "10.0_um_count_b"]

    def __init__(self, data: Dict[str, Any]):
        try:
            self.created_at = data['created_at']
            self.parameters = [base.ParamNameValue(name=n, value=data.get(n)) for n in ThingspeakChannel2BResponseModel.FIELDS]
        except KeyError as ke:
            raise SystemExit(f"{ThingspeakChannel2BResponseModel.__name__}: bad sensor data => missing key='{ke!s}'")


RESP_MODEL_TYPE = Union[
    ThingspeakChannel1AResponseModel,
    ThingspeakChannel1BResponseModel,
    ThingspeakChannel2AResponseModel,
    ThingspeakChannel2BResponseModel]


################################ THINGSPEAK RESPONSE MODEL BUILDER CLASS ################################
class ThingspeakAPIResponseModelBuilder(base.BaseResponseModelBuilder):

    def __init__(self, response_model_class=RESP_MODEL_TYPE):
        super(ThingspeakAPIResponseModelBuilder, self).__init__(response_model_class=response_model_class)

    def response(self, parsed_response: Dict[str, Any]) -> List[RESP_MODEL_TYPE]:
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
