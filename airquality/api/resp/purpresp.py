######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 16:06
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any, List
import airquality.api.resp.baseresp as base


################################ PURPLEAIR API RESPONSE MODEL ################################
class PurpleairAPIResponse(base.BaseAPIResponse):

    API_PARAM = ["primary_key_a", 'primary_id_a', 'primary_key_b', 'primary_id_b',
                 'secondary_key_a', 'secondary_id_a', 'secondary_key_b', 'secondary_id_b']

    CHANNELS = ['Primary data - Channel A', 'Primary data - Channel B',
                'Secondary data - Channel A', 'Secondary data - Channel B']

    def __init__(self, data: Dict[str, Any]):
        try:
            self.name = data['name']
            self.sensor_index = data['sensor_index']
            self.latitude = data['latitude']
            self.longitude = data['longitude']
            self.date_created = data['date_created']
            self.parameters = [base.ParamNameValue(name=n, value=data[n]) for n in PurpleairAPIResponse.API_PARAM]
        except KeyError as ke:
            raise SystemExit(f"{PurpleairAPIResponse.__name__}: bad sensor data => missing key='{ke!s}'")


################################ PURPLEAIR DATA EXTRACTOR ################################
class PurpleairAPIResponseBuilder(base.BaseAPIResponseBuilder):

    def __init__(self, api_response_class=PurpleairAPIResponse):
        super(PurpleairAPIResponseBuilder, self).__init__(api_response_class=api_response_class)

    def build(self, parsed_response: Dict[str, Any]) -> List[PurpleairAPIResponse]:
        responses = []
        try:
            for data_packet in parsed_response['data']:
                responses.append(self.api_response_class(dict(zip(parsed_response['fields'], data_packet))))
        except KeyError as ke:
            raise SystemExit(f"{PurpleairAPIResponseBuilder.__name__}: bas sensor data => missing key={ke!s}")
        return responses
