######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 16:06
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any, List
import airquality.api.resp.baseresp as baseresp


################################ PURPLEAIR API RESPONSE ################################
class PurpleairResponse(baseresp.BaseResponse):

    CHANNEL_PARAM = [{'name': 'Primary data - Channel A', 'key': 'primary_key_a', 'id': 'primary_id_a'},
                     {'name': 'Primary data - Channel B', 'key': 'primary_key_b', 'id': 'primary_id_b'},
                     {'name': 'Secondary data - Channel A', 'key': 'secondary_key_a', 'id': 'secondary_id_a'},
                     {'name': 'Secondary data - Channel B', 'key': 'secondary_key_b', 'id': 'secondary_id_b'}]

    def __init__(self, data: Dict[str, Any]):
        try:
            self.name = data['name']
            self.sensor_index = data['sensor_index']
            self.latitude = data['latitude']
            self.longitude = data['longitude']
            self.date_created = data['date_created']
            self.data = data
        except KeyError as ke:
            raise SystemExit(f"{PurpleairResponse.__name__}: bad sensor data => missing key='{ke!s}'")


################################ PURPLEAIR RESPONSE BUILDER ################################
class PurpleairResponseBuilder(baseresp.BaseResponseBuilder):

    def __init__(self, api_response_class=PurpleairResponse):
        super(PurpleairResponseBuilder, self).__init__(api_response_class=api_response_class)

    def build(self, parsed_response: Dict[str, Any]) -> List[PurpleairResponse]:
        responses = []
        try:
            for data_packet in parsed_response['data']:
                responses.append(self.api_response_class(dict(zip(parsed_response['fields'], data_packet))))
        except KeyError as ke:
            raise SystemExit(f"{PurpleairResponseBuilder.__name__}: bas sensor data => missing key={ke!s}")
        return responses
