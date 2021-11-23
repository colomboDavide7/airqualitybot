######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 16:06
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any, List
import airquality.api.model.baseresp as base


################################ PURPLEAIR API RESPONSE MODEL ################################
class PurpleairAPIResponseModel(base.BaseResponseModel):

    def __init__(self, data: Dict[str, Any]):
        try:
            self.name = data['name']
            self.sensor_index = data['sensor_index']
            self.latitude = data['latitude']
            self.longitude = data['longitude']
            self.date_created = data['date_created']
            self.primary_key_a = data['primary_key_a']
            self.primary_id_a = data['primary_id_a']
            self.primary_key_b = data['primary_key_b']
            self.primary_id_b = data['primary_id_b']
            self.secondary_key_a = data['secondary_key_a']
            self.secondary_id_a = data['secondary_id_a']
            self.secondary_key_b = data['secondary_key_b']
            self.secondary_id_b = data['secondary_id_b']
        except KeyError as ke:
            raise SystemExit(f"{PurpleairAPIResponseModel.__name__}: bad sensor data => missing key='{ke!s}'")


################################ PURPLEAIR DATA EXTRACTOR ################################
class PurpleairAPIResponseModelBuilder(base.BaseResponseModelBuilder):

    def __init__(self, response_model_class=PurpleairAPIResponseModel):
        super(PurpleairAPIResponseModelBuilder, self).__init__(response_model_class=response_model_class)

    def response(self, parsed_response: Dict[str, Any]) -> List[PurpleairAPIResponseModel]:
        responses = []
        try:
            for data_packet in parsed_response['data']:
                responses.append(self.response_model_class(dict(zip(parsed_response['fields'], data_packet))))
        except KeyError as ke:
            raise SystemExit(f"{PurpleairAPIResponseModelBuilder.__name__}: bas sensor data => missing key={ke!s}")
        return responses
