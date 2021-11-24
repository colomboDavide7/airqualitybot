######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 16:08
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any, List
import airquality.api.resp.baseresp as baseresp


################################ ATMOTUBE API RESPONSE MODEL ################################
class AtmotubeResponse(baseresp.BaseResponse):

    ATMOTUBE_FIELDS = ["voc", "pm1", "pm25", "pm10", "t", "h", "p"]

    def __init__(self, data: Dict[str, Any]):
        self.time = data.get('time')
        self.parameters = [baseresp.ParamNameValue(name=n, value=data.get(n)) for n in AtmotubeResponse.ATMOTUBE_FIELDS]
        self.lat = data.get('coords')['lat']
        self.lon = data.get('coords')['lon']


################################ ATMOTUBE RESPONSE MODEL BUILDER CLASS ################################
class AtmotubeResponseBuilder(baseresp.BaseResponseBuilder):

    def __init__(self, api_response_class=AtmotubeResponse):
        super(AtmotubeResponseBuilder, self).__init__(api_response_class=api_response_class)

    def build(self, parsed_response: Dict[str, Any]) -> List[AtmotubeResponse]:
        responses = []
        try:
            for item in parsed_response['data']['items']:
                responses.append(self.api_response_class(item))
        except KeyError as ke:
            raise SystemExit(f"{AtmotubeResponseBuilder.__name__}: bad sensor data => missing key={ke!s}")
        return responses
