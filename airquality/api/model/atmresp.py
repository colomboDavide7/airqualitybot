######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 16:08
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any, List
import airquality.api.model.baseresp as base


################################ ATMOTUBE API RESPONSE MODEL ################################
class AtmotubeResponseModel(base.BaseResponseModel):

    ATMOTUBE_FIELDS = ["voc", "pm1", "pm25", "pm10", "t", "h", "p"]

    def __init__(self, data: Dict[str, Any]):
        self.time = data.get('time')
        self.parameters = [base.ParamNameValue(name=n, value=data.get(n)) for n in AtmotubeResponseModel.ATMOTUBE_FIELDS]
        self.lat = data.get('coords')['lat']
        self.lon = data.get('coords')['lon']


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
