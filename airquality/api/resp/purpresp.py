######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 16:06
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any, List
import airquality.api.resp.resp as resp


################################ PURPLEAIR API RESPONSE ################################
class PurpAPIResp(resp.APIResp):

    CHANNEL_PARAM = [{'name': 'Primary data - Channel A', 'key': 'primary_key_a', 'id': 'primary_id_a'},
                     {'name': 'Primary data - Channel B', 'key': 'primary_key_b', 'id': 'primary_id_b'},
                     {'name': 'Secondary data - Channel A', 'key': 'secondary_key_a', 'id': 'secondary_id_a'},
                     {'name': 'Secondary data - Channel B', 'key': 'secondary_key_b', 'id': 'secondary_id_b'}]

    TYPE = "Purpleair/Thingspeak"

    def __init__(self, data: Dict[str, Any]):
        try:
            self.name = data['name']
            self.sensor_index = data['sensor_index']
            self.latitude = data['latitude']
            self.longitude = data['longitude']
            self.date_created = data['date_created']
            self.data = data
        except KeyError as ke:
            raise SystemExit(f"{PurpAPIResp.__name__}: bad API response => missing key='{ke!s}'")


################################ PURPLEAIR RESPONSE BUILDER ################################
class PurpAPIRespBuilder(resp.APIRespBuilder):

    def __init__(self, api_resp_cls=PurpAPIResp):
        super(PurpAPIRespBuilder, self).__init__(api_resp_cls=api_resp_cls)

    def build(self, parsed_resp: Dict[str, Any]) -> List[PurpAPIResp]:
        responses = []
        try:
            for data_packet in parsed_resp['data']:
                responses.append(self.api_response_class(dict(zip(parsed_resp['fields'], data_packet))))
        except KeyError as ke:
            raise SystemExit(f"{PurpAPIRespBuilder.__name__}: bad API response => missing key={ke!s}")
        return responses
