######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 16:08
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any, List
import airquality.api.resp.resp as resp


################################ ATMOTUBE API RESPONSE MODEL ################################
class AtmoAPIResp(resp.APIResp):

    FIELDS = ["voc", "pm1", "pm25", "pm10", "t", "h", "p"]

    def __init__(self, data: Dict[str, Any]):
        self.time = data.get('time')
        self.measures = [resp.ParamNameValue(name=n, value=data.get(n)) for n in AtmoAPIResp.FIELDS]
        self.lat = data.get('coords')['lat']
        self.lon = data.get('coords')['lon']


################################ ATMOTUBE RESPONSE MODEL BUILDER CLASS ################################
class AtmoAPIRespBuilder(resp.APIRespBuilder):

    def __init__(self, api_resp_cls=AtmoAPIResp):
        super(AtmoAPIRespBuilder, self).__init__(api_resp_cls=api_resp_cls)

    def build(self, parsed_resp: Dict[str, Any]) -> List[AtmoAPIResp]:
        responses = []
        try:
            for item in parsed_resp['data']['items']:
                responses.append(self.api_response_class(item))
        except KeyError as ke:
            raise SystemExit(f"{AtmoAPIRespBuilder.__name__}: bad API response => missing key={ke!s}")
        return responses
