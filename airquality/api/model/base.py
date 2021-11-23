######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 16:39
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import Union, Dict, Any, List
import airquality.api.model.purpleair as p
import airquality.api.model.atmotube as a
import airquality.api.model.thingspeak as t

# DEFINE A UNION TYPE FOR THE RESPONSE MODEL
RESP_MODEL_TYPE = Union[
    p.PurpleairAPIResponseModel,
    a.AtmotubeResponseModel,
    t.ThingspeakChannel1AResponseModel,
    t.ThingspeakChannel1BResponseModel,
    t.ThingspeakChannel2AResponseModel,
    t.ThingspeakChannel2BResponseModel
]


class BaseResponseModelBuilder(abc.ABC):

    def __init__(self, response_model_class=RESP_MODEL_TYPE):
        self.response_model_class = response_model_class

    @abc.abstractmethod
    def response(self, parsed_response: Dict[str, Any]) -> List[RESP_MODEL_TYPE]:
        pass
