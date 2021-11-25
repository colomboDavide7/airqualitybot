######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 16:39
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import Dict, Any, List


class APIResp(abc.ABC):
    pass


class ParamNameValue:

    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value


class APIRespBuilder(abc.ABC):

    def __init__(self, api_resp_cls=APIResp):
        self.api_response_class = api_resp_cls

    @abc.abstractmethod
    def build(self, parsed_resp: Dict[str, Any]) -> List[APIResp]:
        pass
