######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 16:39
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import Dict, Any, List


class BaseResponseModel(abc.ABC):
    pass


class ParamNameValue:

    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value


class BaseResponseModelBuilder(abc.ABC):

    def __init__(self, response_model_class=BaseResponseModel):
        self.response_model_class = response_model_class

    @abc.abstractmethod
    def response(self, parsed_response: Dict[str, Any]) -> List[BaseResponseModel]:
        pass
