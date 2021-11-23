######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 16:08
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any, List
import airquality.api.model.base as base


################################ ATMOTUBE API RESPONSE MODEL ################################
class AtmotubeResponseModel:

    def __init__(self, data: Dict[str, Any]):
        try:
            self.time = data['time']
            self.voc = data['voc']
            self.pm1 = data['pm1']
            self.pm25 = data['pm25']
            self.pm10 = data['pm10']
            self.temp = data['t']
            self.hum = data['h']
            self.press = data['p']
        except KeyError as ke:
            raise SystemExit(f"{AtmotubeResponseModel.__name__}: bad sensor data => missing key='{ke!s}'")


################################ ATMOTUBE RESPONSE MODEL BUILDER CLASS ################################
class AtmotubeAPIResponseModelBuilder(base.BaseResponseModelBuilder):

    def __init__(self, response_model_class=AtmotubeResponseModel):
        super(AtmotubeAPIResponseModelBuilder, self).__init__(response_model_class=response_model_class)

    def response(self, parsed_response: Dict[str, Any]) -> List[AtmotubeResponseModel]:
        responses = []
        try:
            for item in parsed_response['data']['items']:
                responses.append(self.response_model_class(item))
        except KeyError as ke:
            raise SystemExit(f"{AtmotubeAPIResponseModelBuilder.__name__}: bad sensor data => missing key={ke!s}")
        return responses
