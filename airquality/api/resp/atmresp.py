######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 16:08
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any, List
import airquality.api.resp.baseresp as base


################################ ATMOTUBE API RESPONSE MODEL ################################
class AtmotubeAPIResponse(base.BaseAPIResponse):

    ATMOTUBE_FIELDS = ["voc", "pm1", "pm25", "pm10", "t", "h", "p"]

    def __init__(self, data: Dict[str, Any]):
        self.time = data.get('time')
        self.parameters = [base.ParamNameValue(name=n, value=data.get(n)) for n in AtmotubeAPIResponse.ATMOTUBE_FIELDS]
        self.lat = data.get('coords')['lat']
        self.lon = data.get('coords')['lon']


################################ ATMOTUBE RESPONSE MODEL BUILDER CLASS ################################
class AtmotubeAPIResponseBuilder(base.BaseAPIResponseBuilder):

    def __init__(self, api_response_class=AtmotubeAPIResponse):
        super(AtmotubeAPIResponseBuilder, self).__init__(api_response_class=api_response_class)

    def build(self, parsed_response: Dict[str, Any]) -> List[AtmotubeAPIResponse]:
        responses = []
        try:
            for item in parsed_response['data']['items']:
                responses.append(self.api_response_class(item))
        except KeyError as ke:
            raise SystemExit(f"{AtmotubeAPIResponseBuilder.__name__}: bad sensor data => missing key={ke!s}")
        return responses
